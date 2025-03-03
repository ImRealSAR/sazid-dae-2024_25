import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import axios from 'axios';
import MessageBubble from './MessageBubble'; // Import the new component

const API_KEY = 'AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE';
const API_URL = 'https://api.gemini.com/v1/chat'; // Adjust based on Gemini's actual API endpoint

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (input.trim() === '') return;
    const userMessage = { id: messages.length, text: input, sender: 'user' };
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(
        API_URL,
        { message: input },
        { headers: { Authorization: `Bearer ${API_KEY}` } }
      );

      const aiMessage = { id: messages.length + 1, text: response.data.reply, sender: 'ai' };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error('Error fetching AI response:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => <MessageBubble text={item.text} sender={item.sender} />}
      />
      <TextInput style={styles.input} value={input} onChangeText={setInput} placeholder='Type a message' />
      <Button title={loading ? 'Thinking...' : 'Send'} onPress={sendMessage} disabled={loading} />
    </View>
  );
};

const HomeScreen = ({ navigation }) => (
  <View style={styles.container}>
    <Text>Welcome to the AI Chatbot!</Text>
    <Button title='Go to Chat' onPress={() => navigation.navigate('Chat')} />
  </View>
);

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name='Home' component={HomeScreen} />
        <Stack.Screen name='Chat' component={ChatScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center', alignItems: 'center' },
  input: { borderWidth: 1, width: '80%', padding: 10, margin: 10 },
});

