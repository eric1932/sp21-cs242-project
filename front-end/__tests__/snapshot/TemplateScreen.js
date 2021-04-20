import * as React from 'react';
import renderer from 'react-test-renderer';
import TemplateScreen from "../../src/screens/TemplateScreen";

it('TemplateScreen', () => {
  const tree = renderer.create(
    <TemplateScreen />
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
