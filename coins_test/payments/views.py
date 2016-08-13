from django.shortcuts import render


@authentication_classes((SignatureAuthentication, ))
class FactList(generics.ListAPIView):
    """
    List of all `Facts`
    """
    queryset = Fact.objects.all()
    serializer_class = FactSerializer


@authentication_classes((SignatureAuthentication, ))
class FactDetail(generics.RetrieveAPIView):
    queryset = Fact.objects.all()
    serializer_class = FactSerializer

    def get_object(self, queryset=None):
        if not queryset:
            working_set = self.get_queryset()
        else:
            working_set = queryset
        code = self.kwargs['code']
        section = self.kwargs['section']
        return working_set.get(code=code, section__name=section)

    def get(self, request, *args, **kwargs):
        """
        One `Fact` from given *section* and *code*
        ---
        parameters:
            - name: section
              type: string
              paramType: path
              required: true
              description: Name of fact Section
            - name: code
              type: integer
              paramType: path
              required: true
              description: Fact code
        """
        return super(FactDetail, self).get(request, *args, **kwargs)