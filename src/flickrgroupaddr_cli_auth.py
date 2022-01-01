#!/usr/bin/python3

import argparse
import flickrapi
import json



def _get_flickr_user_access_token( api_key_info ):
    flickrapi_handle = flickrapi.FlickrAPI( api_key_info[ 'api_key' ], api_key_info[ 'api_secret' ] )

    # Get a request token
    flickrapi_handle.get_request_token( oauth_callback='oob' )

    # Get the authorize URL that the user needs to go to on their own machine
    flickr_authorize_url = flickrapi_handle.auth_url( perms='write' )

    print( f"Go to this URL and clicky the buttons: {flickr_authorize_url}" )

    flickr_verifier_code = str( input( 'Verifier code given by Flickr: ' ) )

    # Now trade the request token for a long-lived access token
    flickrapi_handle.get_access_token( flickr_verifier_code )


    print( "Auth data is stored in ~/.flickr SQLite database" )




def _get_api_keys( args ):
    with open( args.api_key_json, "r" ) as api_key_handle:
        api_key_info = json.load( api_key_handle )

    return api_key_info


def _read_args():
    arg_parser = argparse.ArgumentParser(description="FlickrGroupAddr CLI tool to get API key")
    arg_parser.add_argument( "api_key_json", help="JSON file with API key and secret" )

    return arg_parser.parse_args()


def _main():
    args = _read_args()
    api_key_info = _get_api_keys( args )
    _get_flickr_user_access_token( api_key_info )



if __name__ == "__main__":
    _main()

