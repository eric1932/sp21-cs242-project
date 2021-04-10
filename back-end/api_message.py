"""
API messages
"""
from fastapi import status
from fastapi.responses import JSONResponse

resp_404_no_such_user = JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                     content={"error": "user not exist"})

resp_403_password_mismatch = JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                          content={"error": "invalid username or password"})

resp_200_logout_success = JSONResponse(status_code=status.HTTP_200_OK,
                                       content={"success": "logout"})

resp_401_logout_fail = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                    content={"error": "invalid token to logout"})
