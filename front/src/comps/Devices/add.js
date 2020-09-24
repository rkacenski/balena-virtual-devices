import React, { useState, useEffect } from 'react';
import { Flex, Box, Button, Modal, Input, Select } from 'rendition';

export default ({appList}) => {
  const [show, setShow] = useState(false);
  const [formData, setFormData] = useState({
    device_name: null,
    application: null
  });


  // useEffect(() => { 
  // }, [])

  function formSubmit() {
    console.log(formData);
    fetch('http://localhost:5000/devices/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(json => {
      console.log(json);
    });
    setShow(false)
  }

  return (
    <div>
      <Button primary onClick={() => setShow(true)}>
        + Add device
      </Button>
      {show && (
        <Modal
          title='Add virtual device'
          cancel={() => {
            setShow(false)
          }}
          done={(x) => {
            formSubmit()
          }}
        >
          <label>
            <div>Name as you want it on Balena Cloud</div>
            <Input
              m={2}
              placeholder='Device Name'
              type='text'
              name="device_name"
              onChange={ ({target}) => 
                setFormData({ ...formData,
                  [target.name]: target.value
                }) 
              }
            />
          </label>

          <Select
            m={2}
            placeholder='Passed an object as option'
            options={appList}
            labelKey='applicationId'
            onChange={({ value }) => {
              setFormData({ ...formData,
                application: value.file_name
              }) 
            }}
          />
        </Modal>
      )}
    </div>
  );
}