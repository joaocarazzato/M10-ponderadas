import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_app/api/storage_api.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;


class PaginaCamera extends StatefulWidget {
  static const route = '/camera';
  const PaginaCamera({super.key});

  @override
  State<PaginaCamera> createState() => _PaginaCamera();

  }

class _PaginaCamera extends State<PaginaCamera> {
  String info = "";
  Uint8List? pickedFile;


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Mudança de imagem"),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        ),
      body: 
        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (pickedFile != null)
              Expanded(
              child : Container(
              child: Image.memory(
                pickedFile!,
                fit: BoxFit.contain,
              ),
             ),
            ),
            Text(info),
              ElevatedButton(
                onPressed: () => _selectAndShareImage(context),
                // onPressed: () => teste(),

                child: Text('Selecione sua imagem'),
              ),
            ],
          ),
        ),
    );
  }

  Future<void> teste() async {
    var id = await StorageApi().getId();
    print("teste");
    print("id: $id");
  }

  Future<void> _selectAndShareImage(BuildContext context) async {
    final picker = ImagePicker();
    XFile? xfile = await picker.pickImage(source: ImageSource.gallery);
    if (xfile != null) {
      File file = File(xfile.path);
      var request = http.MultipartRequest("POST", Uri.parse("http://10.0.2.2:8000/image/upload_white"));
      String userId = await StorageApi().getId();
      request.fields['user_id'] = userId;
      request.files.add(http.MultipartFile.fromBytes("file", File(file.path).readAsBytesSync(),filename: file.path));
      var response = await request.send();
      print(response);
      if (response.statusCode == 200) {
        // final responseData = await http.Response.fromStream(response);
        setState(() {
          info = "Sucesso! Sua imagem foi adicionada ao processamento! Te avisaremos quando estiver concluída!";
          // pickedFile = responseData.bodyBytes;
        });
      } else {
        info = "Ocorreu um erro: ${response.statusCode}";
      }
    }
    }
}