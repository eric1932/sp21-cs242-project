import * as React from 'react';
import renderer from 'react-test-renderer';
import TaskScreen from "../../src/screens/TaskScreen";

it('TaskScreen', () => {
  const tree = renderer.create(
    <TaskScreen />
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
