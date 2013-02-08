#!/usr/bin/python3 -tt

# Copyright 2013 Jussi Pakkanen

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, pickle, os, shutil, subprocess

class InstallData():
    def __init__(self, depfixer, dep_prefix):
        self.targets = []
        self.depfixer = depfixer
        self.dep_prefix = dep_prefix

def do_install(datafilename):
    ifile = open(datafilename, 'rb')
    d = pickle.load(ifile)
    for t in d.targets:
        fullfilename = t[0]
        outdir = t[1]
        fname = os.path.split(fullfilename)[1]
        outname = os.path.join(outdir, fname)
        print('Installing %s to %s' % (fname, outdir))
        os.makedirs(outdir, exist_ok=True)
        shutil.copyfile(fullfilename, outname)
        shutil.copystat(fullfilename, outname)
        p = subprocess.Popen([d.depfixer, outname, d.dep_prefix], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        (stdo, stde) = p.communicate()
        if p.returncode != 0:
            print('Could not fix dependency info.\n')
            print('Stdout:\n%s\n' % stdo.decode())
            print('Stderr:\n%s\n' % stde.decode())
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Installer script for Builder. Do not run on your own, mmm\'kay?')
        print('%s [install info file]' % sys.argv[0])
    datafilename = sys.argv[1]
    do_install(datafilename)
