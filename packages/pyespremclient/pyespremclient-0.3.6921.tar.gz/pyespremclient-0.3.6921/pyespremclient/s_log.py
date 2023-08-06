
#####################################################################
#
# ESPREM Client Log
#
# Project   : PYESPREMCLIENT
# Author(s) : Zafar Iqbal < zaf@saparc.gr >
# Copyright : (C) 2021 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import json

from . import get_version

#####################################################################

def write( msg_raw ) :

    msg = msg_raw
    if(isinstance(msg,list)):
        msg=msg.tostring()
    if(isinstance(msg,dict)):
        msg=json.dumps(msg)

    with open( "/tmp/pyespremclient.log" , "a+" ) as log :
        log.write( msg + "\n" )

#####################################################################

write( "PYESPREMCLIENT" + get_version( ) )

    