import AsyncStorage from '@react-native-async-storage/async-storage';
import { getToken, saveToken } from '../../src/utils/Storage';

it('test getToken()', async () => {
  await getToken();
  expect(AsyncStorage.getItem).toBeCalledWith('@token');
});

it('test saveToken()', async () => {
  await saveToken('test');
  expect(AsyncStorage.setItem).toBeCalledWith('@token', 'test');
});
