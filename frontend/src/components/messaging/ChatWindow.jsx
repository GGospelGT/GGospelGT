import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  MessageCircle, 
  X, 
  User, 
  Briefcase,
  ArrowLeft,
  MoreVertical,
  RefreshCw
} from 'lucide-react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { messagesAPI } from '../../api/services';
import { useAuth } from '../../contexts/AuthContext';
import { useToast } from '../../hooks/use-toast';

const ChatWindow = ({ 
  jobId, 
  jobTitle,
  otherUser,
  onClose,
  className = "",
  isModal = false
}) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [conversation, setConversation] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const { user } = useAuth();
  const { toast } = useToast();

  // Polling interval for new messages (every 3 seconds)
  const POLL_INTERVAL = 3000;

  const loadMessages = useCallback(async (showLoading = true) => {
    try {
      if (showLoading) setLoading(true);
      else setRefreshing(true);

      const response = await messagesAPI.getJobMessages(jobId);
      setMessages(response.messages || []);
      setConversation(response.conversation);

      // Mark messages as read
      const unreadMessages = response.messages.filter(
        msg => msg.recipient_id === user?.id && msg.status !== 'read'
      );
      
      for (const message of unreadMessages) {
        try {
          await messagesAPI.markMessageAsRead(message.id);
        } catch (error) {
          console.error('Failed to mark message as read:', error);
        }
      }

    } catch (error) {
      console.error('Failed to load messages:', error);
      if (showLoading) {
        toast({
          title: "Failed to load messages",
          description: "There was an error loading the conversation.",
          variant: "destructive",
        });
      }
    } finally {
      if (showLoading) setLoading(false);
      else setRefreshing(false);
    }
  }, [jobId, user?.id, toast]);

  // Initial load
  useEffect(() => {
    if (jobId) {
      loadMessages();
    }
  }, [jobId, loadMessages]);

  // Polling for new messages
  useEffect(() => {
    const interval = setInterval(() => {
      if (jobId && !loading) {
        loadMessages(false);
      }
    }, POLL_INTERVAL);

    return () => clearInterval(interval);
  }, [jobId, loading, loadMessages]);

  const handleMessageSent = (newMessage) => {
    setMessages(prev => [...prev, newMessage]);
  };

  const handleImageClick = (imageUrl) => {
    setSelectedImage(imageUrl);
  };

  const closeImageModal = () => {
    setSelectedImage(null);
  };

  const handleRefresh = () => {
    loadMessages(false);
  };

  if (!jobId) {
    return (
      <div className={`flex items-center justify-center h-64 ${className}`}>
        <div className="text-center">
          <MessageCircle size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold font-montserrat text-gray-900 mb-2">
            Select a conversation
          </h3>
          <p className="text-gray-600 font-lato">
            Choose a job to start messaging.
          </p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Card className={`flex flex-col h-full ${className}`}>
        {/* Chat Header */}
        <CardHeader className="flex-shrink-0 pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {isModal && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className="h-8 w-8 p-0"
                >
                  <ArrowLeft size={16} />
                </Button>
              )}
              
              <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                <User size={20} className="text-gray-500" />
              </div>
              
              <div className="flex-1">
                <CardTitle className="text-lg font-montserrat" style={{color: '#121E3C'}}>
                  {otherUser?.name || 'Unknown User'}
                </CardTitle>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Briefcase size={14} />
                  <span className="font-lato">{jobTitle}</span>
                  <Badge variant="outline" className="text-xs">
                    {otherUser?.role === 'tradesperson' ? 'Tradesperson' : 'Homeowner'}
                  </Badge>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleRefresh}
                disabled={refreshing}
                className="h-8 w-8 p-0"
                title="Refresh messages"
              >
                <RefreshCw size={16} className={refreshing ? 'animate-spin' : ''} />
              </Button>
              
              {!isModal && onClose && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className="h-8 w-8 p-0"
                >
                  <X size={16} />
                </Button>
              )}
            </div>
          </div>
        </CardHeader>

        {/* Messages Area */}
        <CardContent className="flex-1 flex flex-col p-0 min-h-0">
          <MessageList
            messages={messages}
            loading={loading}
            onImageClick={handleImageClick}
          />
        </CardContent>

        {/* Message Input */}
        <div className="flex-shrink-0">
          <MessageInput
            jobId={jobId}
            recipientId={otherUser?.id}
            onMessageSent={handleMessageSent}
            placeholder={`Message ${otherUser?.name || 'user'}...`}
          />
        </div>
      </Card>

      {/* Image Modal */}
      {selectedImage && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
          onClick={closeImageModal}
        >
          <div className="relative max-w-4xl max-h-4xl">
            <Button
              variant="outline"
              size="sm"
              onClick={closeImageModal}
              className="absolute top-2 right-2 bg-white hover:bg-gray-100"
            >
              <X size={16} />
            </Button>
            <img
              src={selectedImage}
              alt="Full size"
              className="max-w-full max-h-full object-contain"
              onClick={(e) => e.stopPropagation()}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWindow;