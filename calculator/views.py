from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import math
import re
from . import models
from . import serializers

@api_view(['POST'])
def calculate(request):
    try:
        data = request.data
        expression = data.get("expression", "")
        mode = data.get("mode", "basic")
        
        # Safe dictionary for scientific functions
        safe_dict = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log, 
            "sqrt": math.sqrt, 
            "pow": math.pow,
            "factorial": math.factorial, 
            "pi": math.pi, 
            "e": math.e
        }

        # Add basic operators to safe_dict if mode is 'scientific'
        if mode == "scientific":
            safe_dict.update({
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y if y != 0 else "Division by zero error",
                
            })
        
        # If mode is 'basic', we only use basic operators (+, -, *, /, %)
        if mode == "basic":
            safe_dict = {key: safe_dict[key] for key in safe_dict if key in ["+", "-", "*", "/","sqrt"]}

        # Calculate the result using eval and safe_dict
        result = eval(expression, {"__builtins__": None}, safe_dict)
        
        # Save the result in CalculationHistory
        models.CalculationHistory.objects.create(expression=expression, result=result)

        return Response({"result": result, "type_expression": expression})

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_history(request):
    history_data = models.CalculationHistory.objects.order_by('-created_at')[:10]
    serializer = serializers.CalculationHistorySerializer(history_data,many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def delete_history(request, id):
    try:
        history_item = models.CalculationHistory.objects.get(id=id)
    except models.CalculationHistory.DoesNotExist:
        return Response({'error': 'History not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CalculationHistorySerializer(history_item)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        history_item.delete()
        return Response({'message': 'History deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'DELETE'])
def delete_all_history(request):
    try:
        history_data = models.CalculationHistory.objects.all()
    except models.CalculationHistory.DoesNotExist:
        return Response({'error': 'History not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CalculationHistorySerializer(history_data,many=True)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        history_data.delete()
        return Response({'message': 'All history deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    