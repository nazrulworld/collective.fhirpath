#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import aiofiles
import aiohttp
import asyncio
import json
import logging
import os
import pathlib
import sys
import time
import uuid

SITE_URL = os.environ.get("FHIRPATH_SITE_URL", "http://localhost:8989/Plone")
FHIR_SERVICE_NAME = "@fhir"
SATAIC_FHIR_RESOURCE_DIR = (
    pathlib.Path(os.path.abspath(__name__)).parent.parent.parent
    / "src"
    / "collective"
    / "fhirpath"
    / "tests"
    / "fixture"
    / "FHIR"
)

logger = logging.getLogger("fhir_data_feeder")
AUTH = aiohttp.BasicAuth("admin", "admin")


async def add_batch(count=1):
    """ """
    async with aiohttp.ClientSession() as session:
        for c_ in range(count):
            await run_batch(session)


async def run_batch(session):
    """One batch is consist of  13 FHIR resources"""
    batch = (
        "ChargeItem.json",
        "Encounter.json",
        "Media.json",
        "MedicationRequest.json",
        "Observation.json",
        "Organization.json",
        "ParentTask.json",
        "Patient.json",
        "Practitioner.json",
        "ProcedureRequest_HAQ.json",
        "ProcedureRequest_JOINT.json",
        "SubTask_CRP.json",
        "SubTask_HAQ.json",
    )

    for item in batch:
        async with aiofiles.open(str(SATAIC_FHIR_RESOURCE_DIR / item), "r") as fp:
            data = await fp.read()
            json_data = json.loads(data)
            json_data["id"] = str(uuid.uuid4())
        async with session.post(
            "/".join([SITE_URL, FHIR_SERVICE_NAME, json_data["resourceType"]]),
            headers={"Accept": "application/json"},
            auth=AUTH,
            json=json_data,
        ) as resp:
            result = await resp.json()
            if resp.status != 201:
                sys.stderr.write(
                    "Failed to create {1}/{2}, errors: {0!s}\n".format(
                        result, json_data["resourceType"], json_data["id"]
                    )
                )
            else:
                sys.stdout.write(
                    "{0}/{1} created.\n".format(result["resourceType"], result["id"])
                )


async def main(argv):
    """ """
    counts = int(argv[1])
    for x in range(counts):
        sys.stdout.write("Batch no: {0}\n".format(x + 1))
        await add_batch()


if __name__ == "__main__":

    argv = sys.argv
    if len(argv[1:]) < 1:
        raise RuntimeError(
            "First argument is required, value would idicates number of "
            "batch should run"
        )
    start = time.perf_counter()
    asyncio.run(main(argv))
    end = time.perf_counter() - start
    sys.stdout.write(f"Program finished in {end:0.2f} seconds.\n")
    sys.stdout.write(
        "Avg {0:0.2f} seconds taken per batch execution.\n".format(end / float(argv[1]))
    )
