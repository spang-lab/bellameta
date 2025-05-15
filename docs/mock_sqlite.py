# This script generates a mock storage database under ../data/scans.sqlite using functionality of bellastore (https://github.com/spang-lab/bellastore)


import os
from pathlib import Path
from typing import List
from tempfile import TemporaryDirectory
import shutil 
from random import randint

from bellastore.utils.scan import Scan
from bellastore.database.db import Db

def create_scans(path: Path, amount=4) -> List[Scan]:
    '''
    Mocks scans on a specified path.

    The mock scans are just txt files containing content unique for each scan.
    However they carry the file ending .ndpi 

    The filename encodes for patient_id, diagnosis and year.

    Parameters
    -----------
    path : Path
        The shared directory holding the mocked scans
    amount : int
        The amount of scans to be created
    
    Returns
    --------
    List[Scans]
        The list of created scans
    '''

    years = ['2015', '2020', '2021', '2012']
    diag = ['DLBCL', 'FL', 'MCL', 'CLL']
    filenames = []
    for i in range(amount):
        while True:
            filename = f"{randint(1000,9999)}_{diag[randint(0,3)]}_{years[randint(0,3)]}.ndpi"
            if filename not in filenames:
                filenames.append(filename)
                break
    scans = []
    for filename in filenames:
        p = path / filename
        p.write_text(f"Content of {filename}", encoding="utf-8")
        scan = Scan(str(p))
        scans.append(scan)
    return scans

def main():

    # the root of the fs holding both storage and ingress
    root_dir = TemporaryDirectory().name

    # create 100 scans in ingress
    ingress_dir = Path(root_dir) / "example_cohort"
    os.makedirs(ingress_dir)
    create_scans(path=ingress_dir, amount=100)

    db = Db(root_dir=root_dir, ingress_dir=ingress_dir, filename='scans.sqlite')
    db.insert_from_ingress()
    print(f'Generated database')
    print(str(db))

    shutil.move(db.sqlite_path, os.path.join('data', db.filename))

    shutil.rmtree(root_dir)

if __name__ == "__main__":
    main()