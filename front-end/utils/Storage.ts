// ref: https://react-native-async-storage.github.io/async-storage/docs/usage
import AsyncStorage from '@react-native-async-storage/async-storage';

export async function saveToken(token: string): Promise<boolean> {
  try {
    await AsyncStorage.setItem("@token", token)
    return true
  } catch (e) {
    return false
  }
}

export async function getToken(): Promise<string | null> {
  try {
    // getItem may return null!
    return await AsyncStorage.getItem('@token')
  } catch (e) {
    return null;
  }
}
