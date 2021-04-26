import * as React from 'react';
import renderer from 'react-test-renderer';
import ListItem from '../../src/components/ListItem';

it('ListItem', () => {
  const tree = renderer.create(
    <ListItem name="test" value="test" />,
  ).toJSON();

  expect(tree).toMatchSnapshot();
});
