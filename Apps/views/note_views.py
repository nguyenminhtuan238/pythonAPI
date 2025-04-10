from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..Serializers.note_serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework import status
from ..models.note_models import Note
from django.utils.timezone import now


class note_view:
    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def get_note(request):

        serializer = NoteSerializer(Note.objects.all(), many=True)
        return Response(serializer.data)

    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def get_noteid(request):
        user = request.user

        notes = Note.objects.filter(user_id=user)  # Lọc theo user_id
        serializer = NoteSerializer(notes, many=True)  # Serialize danh sách Note
        return Response(serializer.data)

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def create_note(request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = request.user
            notes = Note.objects.filter(user=user.id)  # Lọc theo user_id
            serializerid = NoteSerializer(notes, many=True)  # Serialize danh sách Note
            return Response(serializerid.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["PATCH"])
    @permission_classes([IsAuthenticated])
    def update_note(request, pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(
                {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["DELETE"])
    @permission_classes([IsAuthenticated])
    def delete_note(request, pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(
                {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
            )

        note.delete()
        user = request.user
        notes = Note.objects.filter(user=user.id)  # Lọc theo user_id
        serializer = NoteSerializer(notes, many=True)  # Serialize danh sách Note
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # @api_view(["DELETE"])
    # @permission_classes([IsAuthenticated])
    # def delete_note(request, pk):
    #     try:
    #         note = Note.objects.get(pk=pk)
    #         if note.is_deleted():
    #             return Response(
    #                 {"message": "Note already deleted permanently!"}, status=400
    #             )
    #         note.soft_delete()
    #         return Response(
    #             {
    #                 "message": "Note marked as deleted. You can restore within 5 minutes."
    #             },
    #             status=status.HTTP_204_NO_CONTENT,
    #         )
    #     except Note.DoesNotExist:
    #         return Response(
    #             {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
    #         )

    # @api_view(["POST"])
    # @permission_classes([IsAuthenticated])
    # def delete_restore(request, pk):
    #     try:
    #         note = Note.objects.get(pk=pk)
    #         if not note.is_deleted():
    #             return Response(
    #                 {"message": "Note is not deleted or already restored!"}, status=400
    #             )
    #         note.restore()
    #         return Response(
    #             {"message": "Note  restored successfully!"},
    #             status=status.HTTP_204_NO_CONTENT,
    #         )
    #     except Note.DoesNotExist:
    #         return Response(
    #             {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
    #         )
