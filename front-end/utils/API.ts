import {API_BASE_URL} from "../constants/Networking";

export async function validateUser(username: string, password: string): Promise<string | null> {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  let requestBody = JSON.stringify({
    "username": username,
    "password": password
  });

  let requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: requestBody,
    redirect: 'follow',
  };

  try {
    let response = await fetch(`${API_BASE_URL}/login`, requestOptions)
    if (response.status == 403) {
      return null;
    }
    let loginJson = await response.json()
    return loginJson.token
  } catch (e) {
    return null
  }
}