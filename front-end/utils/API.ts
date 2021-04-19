import {API_BASE_URL} from "../constants/Networking"

export async function validateUser(username: string, password: string): Promise<string | null> {
  let myHeaders = new Headers()
  myHeaders.append("Content-Type", "application/json")

  let requestBody = JSON.stringify({
    "username": username,
    "password": password
  })

  try {
    let response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: myHeaders,
      body: requestBody,
      redirect: 'follow',
    })
    if (response.status == 403) {
      return null
    }
    let loginJson = await response.json()
    return loginJson.token
  } catch (e) {
    return null
  }
}

export async function validateUserToken(token: string): Promise<boolean> {
  var myHeaders = new Headers()
  myHeaders.append("token", token)

  try {
    let response = await fetch("http://127.0.0.1:8000/task", {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    })
    let list = await response.json()
    return list instanceof Array
  } catch (e) {
    return false
  }
}
