import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:firebase_messaging/firebase_messaging.dart';
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
  bool executed = false;

  @override
  Widget build(BuildContext context) {

    final message = ModalRoute.of(context)!.settings.arguments;
    if (message is RemoteMessage && !executed) {
      executed = true;
      if (message.data['user_id'] != null) {
        print("MESSAGE: ${message.data['user_id']}");
        getProcessedImage(message.data['user_id']);
      }
    }
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

  Future<void> getProcessedImage(String id) async {
    var resposta = await http.post(Uri.parse("http://10.0.2.2:8000/image/get_image"), 
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'id': int.parse(id), 
      })
    );
    if (resposta.statusCode == 200) {
        setState(() {
          pickedFile = resposta.bodyBytes;
        });
    }
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