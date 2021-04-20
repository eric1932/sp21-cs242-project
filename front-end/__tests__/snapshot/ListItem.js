import * as React from 'react';
import renderer from 'react-test-renderer';
import TemplateScreen from '../../src/screens/TemplateScreen';
import ListItem from '../../src/components/ListItem';

it('TemplateScreen', () => {
  const tree = renderer.create(
    <ListItem name="test" value="test" />,
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
