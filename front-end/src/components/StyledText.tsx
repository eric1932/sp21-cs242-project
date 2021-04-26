import * as React from 'react';
import {ReactElement} from 'react';

import {Text, TextProps} from './Themed';

export function MonoText(props: TextProps): ReactElement {
  return <Text {...props} style={[props.style, { fontFamily: 'space-mono' }]} />;
}
