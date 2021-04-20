/**
 * My API handler
 */

import {API_BASE_URL} from "../constants/Networking"
import {userTaskItem} from "../types";


/**
 * Validate username & password and get token if possible
 * @param username
 * @param password
 */
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

/**
 * Translate token into username, if applicable
 * @param token
 */
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

/**
 * Validate if a token is valid
 * @param token
 */
export async function validateUserToken(token: string): Promise<boolean> {
  return await tokenToUsername(token) !== null
}

/**
 * List a user's active tasks
 * @param token
 */
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

/**
 * Logout the user
 * @param token used to authenticate
 * @param fullLogout set true to remove all tokens related to this user
 */
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

/**
 * Get all templates
 */
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

/**
 * Stop & remove a task from user
 * @param token user's access token
 * @param item the task to remove
 */
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
