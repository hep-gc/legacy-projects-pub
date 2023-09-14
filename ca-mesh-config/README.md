Canadian perfSonar Configuration Files 
=============================

The `.conf` file in the repository can be made into `.json` files by running:

    $ /opt/perfsonar_ps/mesh_config/bin/build_json -input <file>.conf -output <file>.json

To build all the json in this repo do:

    $ ./build-jsons.sh

Note that the json files are commited to the reposity for easy access, however
they should always be regenerated before a commit.
