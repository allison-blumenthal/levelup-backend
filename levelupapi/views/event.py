"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
  """Level up event view"""
  
  def retrieve(self, request, pk):
    """Handle GET requests for single event
    
    Returns:
      Response -- JSON serialized event
    """
    
    try:
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
    
  def list(self, request):
    """Handle GET requests to get all events
    
    Returns:
      Response -- JSON serialized list of events
    """
    
    events = Event.objects.all()
    
    game = request.query_params.get('game', None)
    if game is not None:
      events = events.filter(game_id=game)
      
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handle POST operations
    
    Returns -- JSON serialized event instance"""
    
    organizer = Gamer.objects.get(pk=request.data["userId"])
    game = Game.objects.get(pk=request.data["gameId"])
    
    event = Event.objects.create(
      description=request.data["description"],
      date=request.data["date"],
      time=request.data["time"],
      organizer=organizer,
      game=game,
    )
    serializer = EventSerializer(event)
    return Response(serializer.data)
  
  
  def update(self, request, pk):
    """Handle PUT requests for an event
    
    Returns:
        Response -- Empty body with 204 status code
    """
    
    event = Event.objects.get(pk=pk)
    event.description = request.data["description"]
    event.date = request.data["date"]
    event.time = request.data["time"]
    
    game = Game.objects.get(pk=request.data["game"])
    organizer = Gamer.objects.get(uid=request.data["userId"])
    
    event.game = game
    event.organizer = organizer
    event.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
      event = Event.objects.get(pk=pk)
      event.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
class EventSerializer(serializers.ModelSerializer):
  """JSON serializer for events"""
  
  class Meta:
      model = Event
      fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
      depth = 1
