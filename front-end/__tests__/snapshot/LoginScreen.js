import * as React from 'react';
import renderer from 'react-test-renderer';
import LoginScreen from "../../src/screens/LoginScreen";

const createTestProps = (props) => ({
  navigation: {
    navigate: jest.fn()
  },
  ...props
});

it('LoginScreen', () => {
  const tree = renderer.create(
    <LoginScreen {...createTestProps({})} />
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
