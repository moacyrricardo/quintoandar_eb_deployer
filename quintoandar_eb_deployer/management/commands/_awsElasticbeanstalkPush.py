#!/usr/bin/env python

#-*-python-*-

# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy
# of the License is located at
#
#   http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.

import argparse 
from aws.dev_tools import * 

if __name__ == "__main__":

    env_message = """ENVIRONMENT is the name of an AWS Elastic Beanstalk environment. When this 
    option is used, the command updates the named environment instead of the default environment. 
    The default environment can be set by editing .elasticbeanstalk/config in the root of your 
    repository by running "git aws.config" """

    cmt_message = """COMMIT identifies a commit in the repository. For example, HEAD identifies
    the commit that is currently checked out, or a SHA1 (possibly abbreviated) can be used to 
    identify a specific commit from the history. When this option is used, the command uses the named
    commit instead of HEAD to create the version to be deployed to your environment. See the help for
    "git rev-parse" for a description of all the supported formats for identifying commits"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--environment", help=env_message)
    parser.add_argument("-c", "--commit", help=cmt_message)

    parser.add_argument('-a','--access-key')
    parser.add_argument('-s','--secret-key')
    parser.add_argument('-r','--region')
    parser.add_argument('-w','--environment-name')
    parser.add_argument('-x','--application-name')

    args = parser.parse_args()
    opts = {}
    dev_tools = DevTools(args.access_key, args.secret_key, args.region, args.environment_name, args.application_name)

    if args.environment:
	opts["env"] = args.environment

    if args.commit:
	if not dev_tools.commit_exists(args.commit):
	    exit(1)

	cmt_type = dev_tools.git_object_type(args.commit)
	if "commit" != cmt_type:
	    sys.stderr.write("{0} is a {1}. The value of the --commit option must refer to commit".format(args.commit, cmt_type))
	    exit(1)

	opts["commit"] = dev_tools.commit_id(args.commit)

    dev_tools.push_changes(opts.get("env"), opts.get("commit"))
    print "\033[92mEnvironment update initiated successfully.\033[0m"
