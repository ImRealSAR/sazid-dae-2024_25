import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Project Initialization: React Native app setup with Expo

// UI Components: ChatScreen component to handle user messages
const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // State Management: Using useState to manage chat messages dynamically
  const sendMessage = async () => {
    if (input.trim() === '') return;
    const userMessage = { id: messages.length, text: input, sender: 'user' };
    setMessages([...messages, userMessage]);
    setInput('');

    // API Integration: Mock API response for AI-generated reply
    const aiMessage = { id: messages.length + 1, text: 'AI Response', sender: 'ai' };
    setTimeout(() => setMessages([...messages, userMessage, aiMessage]), 1000);
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <Text style={item.sender === 'user' ? styles.userText : styles.aiText}>{item.text}</Text>
        )}
      />
      <TextInput style={styles.input} value={input} onChangeText={setInput} placeholder='Type a message' />
      <Button title='Send' onPress={sendMessage} />
    </View>
  );
};

// Navigation: HomeScreen component with navigation to ChatScreen
const HomeScreen = ({ navigation }) => (
  <View style={styles.container}>
    <Text>Welcome to the AI Chatbot!</Text>
    <Button title='Go to Chat' onPress={() => navigation.navigate('Chat')} />
  </View>
);

const Stack = createStackNavigator();

// Navigation: Setting up stack navigator for multiple screens
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

// Styling: Applying styles to make UI visually appealing
const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center', alignItems: 'center' },
  input: { borderWidth: 1, width: '80%', padding: 10, margin: 10 },
  userText: { alignSelf: 'flex-end', backgroundColor: '#ADD8E6', padding: 5, margin: 5 },
  aiText: { alignSelf: 'flex-start', backgroundColor: '#D3D3D3', padding: 5, margin: 5 },
});
