
#####################################################################
#
# ESPREM Client 
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

import os
import re
import io
import json
from pathlib import Path

import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout 

####################################################################

def esprem_rpc( apiendpoint : str , endpoint: str, params_dict , rq_id : int = 0 , timeout = 60 ) :

    headers = { "content-type" : "application/json" }
    
    payload = {
                "method" : endpoint ,
                "params": params_dict ,
                "jsonrpc": "2.0" ,
                "id": rq_id ,
    }

    ################################################################

    try :

        response = requests.post( apiendpoint , json = payload , headers = headers , timeout = timeout )

        if( response.status_code != 200 ) :

            response = {
                            "_error" : {
                                "error" : True ,
                                "error_code" : "status_code" ,
                                "error_msg" : response.text ,
                            }
            }    

            return( response )    

    except requests.ConnectionError as e :

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "ConnectionError" ,
                            "error_msg" : str( e ) ,
                        }
        }    

        return( response )    

    except requests.HTTPError as e :

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "HTTPError" ,
                            "error_msg" : str( e ) ,
                        }
        }    

        return( response )    

    except requests.exceptions.InvalidSchema as e :

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "InvalidSchema" ,
                            "error_msg" : str( e ) ,
                        }
        
        }    

        return( response )   

    except requests.exceptions.InvalidURL as e :

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "InvalidURL " ,
                            "error_msg" : str(e) ,
                        }
        }    

        return( response )    

    except requests.exceptions.MissingSchema as e :

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "MissingSchema " ,
                            "error_msg" : str( e ) ,
                        }
        }    

        return( response )    

    #except( ConnectTimeout, HTTPError, ReadTimeout, Timeout ) :

    ################################################################

    response = response.json( )

    if( "result" in response ) :
        return( response[ "result" ] )
    
    ################################################################

    return( response[ "error" ] )
