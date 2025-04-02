import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const MessageBubble = ({ text, sender }) => {
  return (
    <View style={[styles.bubble, sender === 'user' ? styles.user : styles.ai]}>
      <Text>{text}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  bubble: {
    margin: 5,
    padding: 10,
    borderRadius: 10,
    maxWidth: '80%',
  },
  user: {
    alignSelf: 'flex-end',
    backgroundColor: '#DCF8C6',
  },
  ai: {
    alignSelf: 'flex-start',
    backgroundColor: '#ECECEC',
  },
});

export default MessageBubble;
