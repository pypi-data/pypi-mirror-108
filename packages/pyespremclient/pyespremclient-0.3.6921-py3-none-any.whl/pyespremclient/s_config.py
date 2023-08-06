
#####################################################################
#
# ESPREM Client Config
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

from . import s_log  

#####################################################################

config = { }

#####################################################################

def set( config_key , config_val ) :
    global config
    config[ config_key ] = config_val

def get( config_key ) :
    return config[config_key]

def init( config_path , config_key ) :

    global config

    #s_log.write(os.getcwd()+","+config_path)
    #s_log.write(os.getcwd())

    try :

        with open( config_path ) as f :
            config_all = json.load( f )
    
    except IOError :

        s_log.write( "ERROR IOError " + config_path )
        return False

    ####################################################################

    if config_key in config_all :
        config = config_all[ config_key ]
    else :
        s_log.write( "ERROR config_key " + config_key )
        return False

    ####################################################################

    s_log.write( "LOADED " + config_path )

    s_log.write( config )
    s_log.write( config[ "url_endpoint" ] )

    return True



    