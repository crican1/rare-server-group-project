from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from views.user_requests import create_user, login_user, get_all_users, get_single_user, update_user, delete_user
from views import(get_all_comments,
                  get_single_comment,
                  create_comment,
                  delete_comment,
                  update_comment,
                  get_all_posts, get_single_post, create_post, delete_post, update_post)

class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            # It's an if..else statement
            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()

            if resource == "comments":
                if id is not None:
                    response = get_single_comment(id)
                else:
                    response = get_all_comments()
                    
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))

        response = ''
        (resource, id ) = self.parse_url(self.path)

        if resource == "login":
            response = login_user(post_body)

        elif resource == "register":
            response = create_user(post_body)

        # Add a new comment to the list. Don't worry about
        # the orange squiggle, you'll define the create_comment
        # function next.
        elif resource == "users":
            response = create_user(post_body)
        elif resource == "comments":
            response = create_comment(post_body)
        elif resource == "posts":
            response = create_post(post_body)

        # Encode the new comment and send in response
        self.wfile.write(response.encode())


    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

         # Parse the URL
        (resource, id) = self.parse_url(self.path)

         # set default value of success
        success = False

        # Delete a single comment from the list
        if resource == "comments":
            success = update_comment(id, post_body)
        if resource == "users":
            success = update_user(id, post_body)
        if resource == "posts":
           success = update_post(id, post_body)
            
        # handle the value of success
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new comment and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
    # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "users":
            delete_user(id)
        # Delete a single comment from the list
        if resource == "comments":
            delete_comment(id)
        elif resource == "posts":
            delete_post(id)

        # Encode the new user and send in response
            self.wfile.write("".encode())

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
