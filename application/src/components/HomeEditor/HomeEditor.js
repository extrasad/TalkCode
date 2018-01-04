import React, { Component } from 'react';
import AceEditor from 'react-ace';

import 'brace/mode/javascript';
import 'brace/theme/github';

class HomeEditor extends Component {
  render() { 
    return ( 
      <AceEditor
      mode="javascript"
      theme="github"
      name="EditorHome"
      fontSize={14}
      showPrintMargin={false}
      showGutter={true}
      highlightActiveLine={false}
      readOnly={true}
      width={'inherit'}
      height={'400px'}
      value={
        this.props.value
      }
      setOptions={{
        showLineNumbers: true,
        tabSize: 2
      }}
      editorProps={{
        $blockScrolling: Infinity
      }}/>
    )
  }
}
 
export default HomeEditor;