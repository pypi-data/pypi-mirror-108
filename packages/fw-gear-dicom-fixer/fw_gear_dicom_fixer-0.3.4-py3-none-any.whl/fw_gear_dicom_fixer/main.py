"""Main module."""

import functools
import logging
import tempfile
import typing as t
import zipfile
from contextlib import contextmanager
from pathlib import Path

from fw_file.dicom import DICOMCollection
from pydicom import config as pydicom_config
from pydicom.datadict import keyword_for_tag

from .callbacks import decode_dcm, setup_callbacks
from .metadata import add_missing_uid, update_modified_dicom_info

log = logging.getLogger(__name__)


def run(dicom: t.Dict, out_dir: Path) -> t.List[t.Dict[str, t.List[str]]]:
    dicom_path = Path(dicom["location"]["path"]).resolve()
    events = []
    with setup_callbacks():
        if zipfile.is_zipfile(str(dicom_path)):
            dcms = DICOMCollection.from_zip(dicom_path, force=True, track=True)
        else:
            dcms = DICOMCollection(dicom_path, force=True, track=True)
        for dcm in dcms:
            decode_dcm(dcm)
            dcm.tracker.trim()
            for element in dcm.tracker.data_elements:
                if element.events:
                    tagname = str(element.tag).replace(",", "")
                    kw = keyword_for_tag(element.tag)
                    if kw:
                        tagname = kw
                    events.append({tagname: [str(ev) for ev in element.events]})
            update_modified_dicom_info(dcm)

    added_uid = add_missing_uid(dcms)

    if (len(events) > 0 and all([len(ev) > 0 for ev in events])) or added_uid:
        log.info(f"Writing output to {out_dir / dicom_path.name}")
        if len(dcms) > 1:
            dcms.to_zip(out_dir / dicom_path.name)
        else:
            dcms[0].save(out_dir / dicom_path.name)

    return events
