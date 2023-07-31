from rest_framework import serializers

from flashcards.models import StudyProgram, FlashCard


class StudyProgramSerializer(serializers.ModelSerializer):
    flashcard_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyProgram
        fields = "__all__"


class FlashCardSerializers(serializers.ModelSerializer):
    # study_program = serializers.HyperlinkedRelatedField(view_name='group-detail', read_only=True)

    #study_program = serializers.StringRelatedField(many=False)

    class Meta:
        model = FlashCard
        fields = '__all__'
        # extra_kwargs = {
        #     'url': {'view_name': 'card-detail'}
        # }
