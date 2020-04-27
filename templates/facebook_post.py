import facebook

# be sure to pip install facebook-sdk==2.0.0

def main():
   # Fill in the values noted in previous steps here
   cfg = {
       "page_id": "1xxxxx48480xxxx",  # Step 1
       "access_token": "xxxxxxxxxxxxxxxxxxxxxxxnp3QApxv12gjGnV99BNnhxxxxxxxxxx"   # Step 3
   }

   api = get_api(cfg)
   msg = "Hello, world!"
   status = api.put_wall_post(msg)


def get_api(cfg):

    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
    if page['id'] == cfg['page_id']:
        page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph


if __name__ == "__main__":
 main()
