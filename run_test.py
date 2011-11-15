#!/usr/local/bin/python
# Small python-script run all tests using ec (the Eiffel compiler) 
# we assume that ec outputs everything in english!
# 
# Code ported from a ruby script by Niklaus Giger

# For the command line options look at
# http://docs.eiffel.com/book/eiffelstudio/eiffelstudio-command-line-options
# we use often the -batch open.
#
# TODO: Fix problems when compiling takes too long and/or there
#       are ec process lingering around from a previous failed build

import os;
import sys;
import tempfile;
import shutil;
import re;
import subprocess;
from time import sleep;

# Override system command.
# run command. if not successful, complain and exit with error
def eval_cmd(cmd):
#  print cmd
  res = subprocess.call (cmd, shell=True)
  if res < 0:
    print "Failed running: %s" % (cmd)
    sys.exit(2)
  return res

def eval_cmd_output(cmd):
#  print cmd
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  if p:
    return p.communicate()[0]
  else:
    print "Failed running: %s" % (cmd)
    sys.exit(2)

def rm_dir(d):
  if os.path.isdir(d):
	shutil.rmtree(d)


def runTestForProject(where):
  if not os.path.isdir(where):
    print "Directory %s does not exist" % (where)
    sys.exit(2)

  # create a temporary file with input for the 
  # interactive mode of ec
  commands2run="T\nE\nq\n"
  fd, fn = tempfile.mkstemp('commands2run')
  f = open(fn, 'w');
  f.write (commands2run)
  f.close()

  os.chdir(where)
  # First we have to remove old compilation
  rm_dir("EIFGENs")
  
  # compile the library
  cmd = "ecb -config %s -target emime -batch -c_compile" % (os.path.join ("library", "emime-safe.ecf"))
  res = eval_cmd(cmd)

  # compile the test
  cmd = "ec -config %s -target test -batch -c_compile" % (os.path.join ("test", "test-safe.ecf"))
  res = eval_cmd(cmd)

   
  logFile = "%s.log" % (__file__)
  sleep(1)
  cmd = "ec -config %s -target test -batch -loop < %s" % (os.path.join ("test", "test-safe.ecf"), fn)
  res_output = eval_cmd_output(cmd)

  lines = re.split ("\n", res_output)
  regexp = "^(\d+) tests total \((\d+) executed, (\d+) failing, (\d+) unresolved\)$"
  p = re.compile (regexp);
  
  m = [];
  for line in lines:
	p_res = p.search(line.strip(), 0)
	if p_res:
		m = [int(p_res.group(1)), int(p_res.group(2)), int(p_res.group(3)), int(p_res.group(4))]
		break

  print "\n"
  if len(m) >= 3 and m[2] == 0 and m[3] == 0:
    print "%i tests completed successfully" % (m[0])
  else:
    print "Failures while running %i failed. %i executed  %i failures  %i unresolved" % (m[0], m[1], m[2], m[3])
    sys.exit(2)

if __name__ == '__main__':
	runTestForProject(os.getcwd())

