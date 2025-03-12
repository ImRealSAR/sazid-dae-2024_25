import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const MessageBubble = ({ text, sender }) => {
  const isUser = sender === 'user';

  return (
    <View style={[styles.bubble, isUser ? styles.userBubble : styles.aiBubble]}>
      <Text style={isUser ? styles.userText : styles.aiText}>{text}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  bubble: {
    maxWidth: '80%',
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
  },
  userBubble: {
    backgroundColor: '#DCF8C6', // Greenish for user messages
    alignSelf: 'flex-end',
  },
  aiBubble: {
    backgroundColor: '#ECECEC', // Light gray for AI messages
    alignSelf: 'flex-start',
  },
  userText: {
    color: 'black',
  },
  aiText: {
    color: 'black',
  },
});

export default MessageBubble;
