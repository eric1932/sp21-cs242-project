/**
 * Learn more about deep linking with React Navigation
 * https://reactnavigation.org/docs/deep-linking
 * https://reactnavigation.org/docs/configuring-links
 */

import * as Linking from 'expo-linking';

export default {
  prefixes: [Linking.makeUrl('/')],
  config: {
    // screens: {
    //   Root: {
    //     screens: {
    //       TabOne: {
    //         screens: {
    //           TaskScreen: 'one',
    //         },
    //       },
    //       TabTwo: {
    //         screens: {
    //           TabTwoScreen: 'two',
    //         },
    //       },
    //     },
    //   },
    //   NotFound: '*',
    // },
    screens: {
      Login: {
        screens: {
          LoginScreen: 'login'
        }
      },
      // NotFound: '*', TODO restore
    }
  },
};
