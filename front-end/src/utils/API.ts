import {API_BASE_URL} from "../constants/Networking"
import {userTaskItem} from "../types";


export async function validateUser(username: string, password: string): Promise<string | null> {
  const myHeaders = new Headers()
  myHeaders.append("Content-Type", "application/json")

  const requestBody = JSON.stringify({
    "username": username,
    "password": password
  })

  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: myHeaders,
      body: requestBody,
      redirect: 'follow',
    })
    if (response.status == 403) {
      return null
    }
    return (await response.json()).token
  } catch (e) {
    return null
  }
}

export async function tokenToUsername(token: string): Promise<string | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/show/${token}`, {
      method: 'GET',
      redirect: 'follow'
    })
    const username = await response.text()
    if (username !== "null" && username !== null) {
      return username.replace(/^"(.*)"$/, '$1');  // strip double quotes
    } else {
      return null
    }
  } catch (e) {
    return null
  }
}

export async function validateUserToken(token: string): Promise<boolean> {
  return await tokenToUsername(token) !== null
}

export async function listTasks(token: string): Promise<userTaskItem[]> {
  const myHeaders = new Headers()
  myHeaders.append("token", token)

  try {
    const response = await fetch(`${API_BASE_URL}/task`, {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    })
    return await response.json()
  } catch (e) {
    return []
  }
}

export async function logoutUser(token: string, fullLogout: boolean): Promise<boolean> {
  const username = await tokenToUsername(token)

  const myHeaders = new Headers();
  myHeaders.append("token", token);

  try {
    if (username) {
      const response = await fetch(
        `${API_BASE_URL}/logout/${username}?full_logout=${fullLogout ? '1' : '0'}`,
        {
          method: 'GET',
          headers: myHeaders,
          redirect: 'follow'
        })
      return response.status === 200
    } else {
      return false
    }
  } catch (e) {
    return false
  }
}

export async function getTemplateList(): Promise<[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/template/list`, {
      method: 'GET',
      redirect: 'follow'
    })
    return await response.json()
  } catch (e) {
    return []
  }
}

export async function deleteTask(token: string, item: userTaskItem): Promise<boolean> {
  const myHeaders = new Headers();
  myHeaders.append("token", token);

  try {
    const response = await fetch(`${API_BASE_URL}/task/remove/${item.apscheduler_id.join('-')}`, {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    })
    return response.status !== 404;
  } catch (e) {
    return false
  }
}
