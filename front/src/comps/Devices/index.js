import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Flex, 
  Box,
  Heading,
  Button
} from 'rendition';

import Add from './add.js'

export default ({ appList }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState([]);

  useEffect(() => { 
    fetch(`http://localhost:5000/devices`)
      .then(res => res.json())
      .then(json => {
        setIsLoading(false)
        setDevices(json) 
      });
  }, [])

  return (
    <Container px={0}>
      <Flex justifyContent='space-between'>
        <Heading.h3>Devices</Heading.h3>
        <Add appList={appList}></Add>
      </Flex>
      <hr/>
      {isLoading && <p>Wait I'm Loading comments for you</p>}

      <Flex flexWrap='wrap'>
      {devices.map((d,index) =>
        <Box key={index} className="device-box">
          <Heading.h4>Device name { d.id } </Heading.h4>
        </Box>
      )}
      </Flex>
    </Container>
  );
}