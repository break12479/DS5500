import { Col, Row, Statistic, Card, Tabs, TimePicker , Button, Select  } from 'antd';
import React, { useState, useEffect } from 'react';
import { Line } from '@ant-design/charts';

const getItems = async() => {

  try{
    const fetchResponse  = await fetch('http://127.0.0.1:5000/api/getSummary')
    const data = await fetchResponse.json();
    console.log(data)
    
    return data
  }
  catch(e){
    return console.log(e)
  }  
};


const { TabPane } = Tabs;

const Dashboard: React.FC = () => {

  const [events, setEvents] = useState(
    [
    {
      time: 1.4,
      rate: 0.51
    },
    {
      time: 2.4,
      rate: 0.5
    },
    {
      time: 2.9,
      rate: 0.54
    },
    {
      time: 3.6,
      rate: 0.53
    },
    {
      time: 4.6,
      rate: 0.52
    },
    {
      time: 4.8,
      rate: 0.45
    },
    {
      time: 5.6,
      rate: 0.53
    },
    {
      time: 6.6,
      rate: 0.42
    },
    {
      time: 7.8,
      rate: 0.45
    },
  ]);
  const [predictions, setPredictions] = useState([]);


  const plotData = [
    {
      time: 1.4,
      rate: 0.51
    },
    {
      time: 2.4,
      rate: 0.5
    },
    {
      time: 2.9,
      rate: 0.54
    },
    {
      time: 3.6,
      rate: 0.53
    },
    {
      time: 4.6,
      rate: 0.52
    },
    {
      time: 4.8,
      rate: 0.45
    },
    {
      time: 5.6,
      rate: 0.53
    },
    {
      time: 6.6,
      rate: 0.42
    },
    {
      time: 7.8,
      rate: 0.45
    },
  ]

  const config = {
    data: events,
    padding: 'auto',
    xField: 'time',
    yField: 'rate',
    xAxis: {
      // type: 'timeCat',
      tickCount: 5,
    },
    smooth: true,
    scale: {
      y: { 
        type: 'linear',
        domain: [0, 1],
      },
    }
  };
  const handleAddEvent = () => {
    // Add event to the events array
    const newEvent = {
      time: 14,
      rate: 0.7,
    };
    setEvents([...events, newEvent]);
  };

  const handlePredict = async () => {
    try {
      // Make request to backend to get predictions
      
    } catch (error) {
      console.error('Error predicting win rates:', error);
    }
  };

  return (
    <>
      <Card>
        <div style={{ marginBottom: '20px' }}>
          <Line {...config} />
        </div>
        <div>
          <Select
            style={{ width: '100px' }}
            placeholder="Select a team"
            optionFilterProp="children"
            options={[
              {
                value: 'red team',
                label: 'red team',
              },
              {
                value: 'blue team',
                label: 'blue team',
              }, 
            ]}
          />
          <Select
            mode="multiple"
            style={{ width: '450px' }}
            placeholder="Select a event"
            optionFilterProp="children"
            options={[
              {
                value: 'ward placement',
                label: 'ward placement',
              },
              {
                value: 'ping',
                label: 'ping',
              }, 
              {
                value: 'kill',
                label: 'kill',
              },
              {
                value: 'dragon',
                label: 'dragon',
              },
              {
                value: 'Baron',
                label: 'Baron',
              },
            ]}
          />
          <TimePicker format={"mm:ss"} showNow={false}/>
          <Button type="primary" onClick={handleAddEvent}>Add Event</Button>
          <Card style={{ height: 200, overflowY: 'auto', marginTop: '20px' }}>
            {events.map((event, index) => (
              <div key={index}>{`${event.time.toLocaleString()}: ${event.rate}`}</div>
            ))}
          </Card>
          
        </div>
          
      </Card> 
      
    </>  

  );
};


export default Dashboard;
