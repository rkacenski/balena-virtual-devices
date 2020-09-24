import React, { useState, useEffect } from 'react';
import { Flex, Card, Button, Modal, List, Txt } from 'rendition';
import { faPlus } from '@fortawesome/free-solid-svg-icons/faPlus'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import Upload from './upload.js'

export default ({ appList }) => {
  const [show, setShow] = useState(false);

  function rowsDisplay(list) {
    if(!list || !list.length) {
      return [ <div>Loading list...</div> ]
    } else {
      return list.map((app,index) => 
        <Flex key={index} justifyContent='space-between'>
          <div>{app.applicationId}</div>
          <div>go to dash</div>
        </Flex>
      )
    }
  }

  return (
    <Card
      m={2}
      width={350}
      title='Application configs'
      rows={ rowsDisplay(appList) }
      cta={
        <Button
          m={2}
          plain
          primary
          icon={<FontAwesomeIcon icon={faPlus} />}
          onClick={ () => setShow(true)}
        >
          Add config
        </Button>
      }
    >
      {show && (
        <Modal
          title='Add application config'
          cancel={() => {
            setShow(false)
          }}
          done={(x) => {
            setShow(false)
          }}
        >
          <List m={3} ordered={true}>
            <Txt>
              Go to Balena Cloud, select the application and go to the "Devices" dashboard page
            </Txt>
            <Txt>
              Click the "Add device button" and under the advanced option select "Download configuration file only", and download it.
            </Txt>
            <Txt>
              Upload that file here
              <Txt>
                <Upload></Upload>
              </Txt>
            </Txt>
          </List>
        </Modal>
      )}
    </Card>
  );
}