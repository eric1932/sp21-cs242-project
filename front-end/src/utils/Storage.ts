/**
 * Async Storage Wrapper
 * ref: https://react-native-async-storage.github.io/async-storage/docs/usage
 */
import AsyncStorage from '@react-native-async-storage/async-storage';

const itemNames = {
  token: '@token'
}

/**
 * Save token to storage
 * @param token token to save
 */
export async function saveToken(token: string): Promise<boolean> {
  try {
    await AsyncStorage.setItem(itemNames.token, token)
    return true
  } catch (e) {
    return false
  }
}

/**
 * Get token from storage
 */
export async function getToken(): Promise<string | null> {
  try {
    // getItem may return null!
    return await AsyncStorage.getItem(itemNames.token)
  } catch (e) {
    return null;
  }
}

/**
 * Remove token from local storage
 */
export async function removeToken(): Promise<void> {
  try {
    await AsyncStorage.removeItem(itemNames.token)
  } catch (e) {
    // do nothing
  }
}
