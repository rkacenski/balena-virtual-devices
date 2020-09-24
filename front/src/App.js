import React, { useEffect, useState } from 'react';
import { Container, Heading, Flex  } from 'rendition';
import Applications from './comps/Applications';
import Devices from './comps/Devices';

export default () => {

  const [appList, setAppList] = useState([]);

  useEffect(() => { 
    fetch(`http://localhost:5000/apps`)
      .then(res => res.json())
      .then(json => {
        setAppList( json )
      });
  }, [])

  const rows = [
    <div>Lorem Ipsum dolor si amet</div>,
    <Flex justifyContent='space-between'>
      <div>Row with</div>
      <div>Flex</div>
    </Flex>,
    <div>Lorem Ipsum dolor si amet</div>
  ]

  return (
    <div>
      <Container my={3} mx={['auto', 15]}>
        <Heading.h2>Balena Virtual Devices</Heading.h2>
      </Container>

        <Flex flexWrap='wrap' alignItems='flex-start' m={2}>
          <Applications appList={appList}></Applications>
          <Devices appList={appList} flex='1' />
        </Flex>
    </div>
  );
}
