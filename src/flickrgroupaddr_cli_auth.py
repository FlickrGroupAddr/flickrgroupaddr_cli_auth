#!/usr/bin/python3

import argparse
import flickrapi
import json
import sqlite3
import os.path



def _display_user_auth_info( user_auth_info ):
    print( f"User auth info:\n{json.dumps(user_auth_info, indent=4, sort_keys=True)}" )


def _get_user_auth_info( args ):
    sqlite_file_path = os.path.join( args.token_cache_dir, "oauth-tokens.sqlite" )

    with sqlite3.connect( sqlite_file_path ) as sqlite_handle: 
        sql_cursor = sqlite_handle.cursor() 
        sql_cursor.execute( "SELECT username, user_nsid, oauth_token, oauth_token_secret FROM oauth_tokens LIMIT 1;" )

        user_auth_row = sql_cursor.fetchone()

        user_auth_info = {
            'username'                  : user_auth_row[0],
            'user_nsid'                 : user_auth_row[1],
            'user_oath_token'           : user_auth_row[2],
            'user_oauth_token_secret'   : user_auth_row[3],
        }

    return user_auth_info


def _get_flickr_user_access_token( args, api_key_info ):
    flickrapi_handle = flickrapi.FlickrAPI( api_key_info[ 'api_key' ], api_key_info[ 'api_secret' ], 
        token_cache_location=args.token_cache_dir )

    # Get a request token
    flickrapi_handle.get_request_token( oauth_callback='oob' )

    # Get the authorize URL that the user needs to go to on their own machine
    flickr_authorize_url = flickrapi_handle.auth_url( perms='write' )

    print( f"Go to this URL and clicky the buttons: {flickr_authorize_url}" )

    flickr_verifier_code = str( input( 'Verifier code given by Flickr: ' ) )

    # Now trade the request token for a long-lived access token
    flickrapi_handle.get_access_token( flickr_verifier_code )


def _get_api_keys( args ):
    with open( args.api_key_json, "r" ) as api_key_handle:
        api_key_info = json.load( api_key_handle )

    return api_key_info


def _read_args():
    arg_parser = argparse.ArgumentParser(description="FlickrGroupAddr CLI tool to get API key")
    arg_parser.add_argument( "api_key_json", help="JSON file with API key and secret" )
    arg_parser.add_argument( "token_cache_dir", help="Directory for oauth tokens SQLite file" )

    return arg_parser.parse_args()


def _main():
    args = _read_args()
    api_key_info = _get_api_keys( args )
    _get_flickr_user_access_token( args, api_key_info )
    user_auth_info = _get_user_auth_info( args )
    _display_user_auth_info( user_auth_info )



if __name__ == "__main__":
    _main()

