import React from 'react';
import { Card, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { 
  User, 
  MessageCircle,
  Clock,
  Image as ImageIcon
} from 'lucide-react';

const ConversationItem = ({ conversation, isSelected, onClick }) => {
  const formatTime = (dateString) => {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    } else if (diffInHours < 168) { // 7 days
      return date.toLocaleDateString('en-GB', { weekday: 'short' });
    } else {
      return date.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short'
      });
    }
  };

  const truncateMessage = (content, maxLength = 50) => {
    if (!content) return '';
    return content.length > maxLength ? `${content.substring(0, maxLength)}...` : content;
  };

  const getLastMessagePreview = (lastMessage) => {
    if (!lastMessage) return 'No messages yet';
    
    if (lastMessage.message_type === 'image') {
      return (
        <div className="flex items-center">
          <ImageIcon size={14} className="mr-1" />
          <span>{lastMessage.content || 'Image'}</span>
        </div>
      );
    }
    
    return truncateMessage(lastMessage.content);
  };

  return (
    <div
      onClick={() => onClick(conversation)}
      className={`p-4 border-b cursor-pointer transition-colors hover:bg-gray-50 ${
        isSelected ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
      }`}
    >
      <div className="flex items-start space-x-3">
        {/* Avatar */}
        <div className="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
          <User size={20} className="text-gray-500" />
        </div>

        {/* Conversation Details */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <h3 className="font-semibold font-montserrat text-gray-900 truncate" style={{color: '#121E3C'}}>
              {conversation.other_user_name}
            </h3>
            <div className="flex items-center space-x-2 flex-shrink-0">
              {conversation.last_message && (
                <span className="text-xs text-gray-500 font-lato">
                  {formatTime(conversation.last_message.created_at)}
                </span>
              )}
              {conversation.unread_count > 0 && (
                <Badge 
                  className="h-5 w-5 p-0 flex items-center justify-center text-xs text-white"
                  style={{backgroundColor: '#E55E55'}}
                >
                  {conversation.unread_count > 99 ? '99+' : conversation.unread_count}
                </Badge>
              )}
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-600 font-lato mb-1 truncate">
                Job: {conversation.job_title}
              </p>
              <div className={`text-sm font-lato truncate ${
                conversation.unread_count > 0 ? 'font-medium text-gray-900' : 'text-gray-600'
              }`}>
                {getLastMessagePreview(conversation.last_message)}
              </div>
            </div>
            
            <Badge variant="outline" className="text-xs ml-2 flex-shrink-0">
              {conversation.other_user_role === 'tradesperson' ? 'Tradesperson' : 'Homeowner'}
            </Badge>
          </div>
        </div>
      </div>
    </div>
  );
};

const ConversationList = ({ 
  conversations = [], 
  selectedConversationId,
  onConversationSelect,
  loading = false,
  className = ""
}) => {
  if (loading) {
    return (
      <div className={`${className}`}>
        <div className="space-y-1">
          {Array.from({ length: 5 }).map((_, index) => (
            <div key={index} className="p-4 border-b animate-pulse">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gray-200 rounded-full"></div>
                <div className="flex-1">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2 mb-1"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!conversations.length) {
    return (
      <div className={`flex items-center justify-center h-64 ${className}`}>
        <div className="text-center">
          <MessageCircle size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold font-montserrat text-gray-900 mb-2">
            No conversations yet
          </h3>
          <p className="text-gray-600 font-lato">
            Start messaging by viewing jobs and quotes.
          </p>
        </div>
      </div>
    );
  }

  // Sort conversations by last message time
  const sortedConversations = [...conversations].sort((a, b) => {
    const aTime = a.last_message ? new Date(a.last_message.created_at) : new Date(a.created_at);
    const bTime = b.last_message ? new Date(b.last_message.created_at) : new Date(b.created_at);
    return bTime - aTime;
  });

  return (
    <div className={className}>
      {sortedConversations.map((conversation) => (
        <ConversationItem
          key={conversation.job_id}
          conversation={conversation}
          isSelected={selectedConversationId === conversation.job_id}
          onClick={onConversationSelect}
        />
      ))}
    </div>
  );
};

export default ConversationList;