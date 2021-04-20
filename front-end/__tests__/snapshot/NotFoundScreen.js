import * as React from 'react';
import renderer from 'react-test-renderer';
import NotFoundScreen from "../../src/screens/NotFoundScreen";

const createTestProps = (props) => ({
  navigation: {
    navigate: jest.fn()
  },
  ...props
});

it('NotFoundScreen', () => {
  const tree = renderer.create(
    <NotFoundScreen {...createTestProps({})}/>
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
