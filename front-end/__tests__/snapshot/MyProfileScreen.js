import * as React from 'react';
import renderer from 'react-test-renderer';
import MyProfileScreen from "../../src/screens/MyProfileScreen";

const createTestProps = (props) => ({
  navigation: {
    navigate: jest.fn()
  },
  ...props
});

it('MyProfileScreen', () => {
  const tree = renderer.create(
    <MyProfileScreen {...createTestProps({})} />
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
