import os
temp_file = 'temp_output.txt'

# Executa o comando e redireciona a saída para o arquivo temporário
os.system(f"""ollama run llama3 "Você é um assistente de previsão de séries temporais encarregado de analisar dados de uma série temporal específica.

A série temporal tem dados de 95 período(s) consecutivos. Cada anotação da série temporal representa a incidência de um evento que ocorre a cada hora.

Por exemplo, um série temporal pode ser representado assim:
[2, 0, 0, 1, 20, 436, 1295, 988, 799, 604, 430, 672, 695, 414, 378, 615, 1011, 1241, 1101, 559, 402, 483, 388, 103]

Seu objetivo é prever a incidência de um evento para as próximas N horas, levando em consideração não apenas os períodos anteriores, mas também o contexto geral.

Para fazer isso com precisão, leve em consideração: 
- Padrões sazonais: Identifique picos em determinados períodos. 
- Variações de Padrões: Padrões podem variar de acordo com o dia da semana ou eventos especiais (feriados).

Regras da Saída:
Após analisar os dados fornecidos e compreender os padrões de tráfego, gere uma previsão para as próximas N horas, com as seguintes regras: 
- A saída deve ser uma lista contendo apenas os valores previstos, sem explicação adicional ou texto introdutório.
- Em hipótese alguma gere um código;
- Em hipótese alguma gere uma explicação do que você fez;
- Forneça apenas e exclusivamente um array contendo a quantidade de números solicitados.
- A previsão deve começar imediatamente após o último dado fornecido.

Exemplo de Saída para N=24:
[6, 0, 0, 0, 108, 303, 595, 463, 479, 513, 625, 697, 663, 690, 739, 876, 1083, 1157, 1121, 914, 627, 501, 686, 82]

Instruções Adicionais:
- Padrões Semanais: Utilize os dados fornecidos para entender padrões sazonais, como picos de incidência em determinados períodos.
- Eventos Especiais: A ocorrência de eventos é significativamente afetada por feriados e outros eventos importantes.
- Dia da Semana: O dia da semana também influencia a ocorrência de eventos. 
- Duração de um evento: A série temporal fornecida representa a ocorrência de um evento a cada hora.

Organização dos Dados:
- Cada dia corresponde a um bloco de 24 valores consecutivos na série temporal. Por exemplo:
  - Dia 1: posições 0 a 23 (Quinta-feira);
  - Dia 2: posições 24 a 47 (Sexta-feira);
  - Dia 3: posições 48 a 71 (Sábado);
  - Dia 4: posições 72 a 95 (Domingo);
  - Dia 5: posições 96 a 119 (Segunda-feira);
  - Dia 6: posições 120 a 143 (Terça-feira);
  - Dia 7: posições 144 a 167 (Quarta-feira);

- E assim por diante.
- A cada 24 valores, ocorre a transição para o próximo dia.
- Períodos em que temos feriado na série temporal:
  - Dia 19: posições 432 a 455 (Segunda-feira);
  - Dia 25: posições 576 a 599 (Domingo);
  - Dia 30: posições 696 a 719 (Sexta-feira);
  - Dia 41: posições 960 a 983 (Terça-feira);
  - Dia 44: posições 1032 a 1055 (Sexta-feira);
  - Dia 52: posições 1224 a 1247 (Sábado);
  - Dia 62: posições 1464 a 1487 (Terça-feira);
  - Dia 88: posições 2088 a 2111 (Domingo);
  - Dia 89: posições 2112 a 2135 (Segunda-feira);


Serie temporal a ser analisada:
[2, 0, 0, 1, 20, 436, 1295, 988, 799, 604, 430, 672, 695, 414, 378, 615, 1011, 1241, 1101, 559, 402, 483, 388, 103, 2, 0, 0, 1, 26, 438, 1310, 1099, 779, 595, 534, 652, 625, 569, 461, 625, 1146, 1314, 1012, 570, 488, 485, 407, 76, 6, 0, 0, 0, 22, 136, 489, 605, 443, 299, 287, 406, 569, 439, 453, 423, 439, 462, 379, 435, 265, 186, 282, 96, 2, 0, 0, 0, 10, 64, 170, 202, 295, 245, 232, 177, 295, 213, 158, 204, 237, 270, 217, 202, 175, 81, 150, 63, 3, 0, 0, 0, 17, 449, 1308, 1230, 840, 520, 480, 585, 602, 464, 443, 524, 1084, 1179, 1178, 657, 484, 515, 406, 62, 2, 0, 0, 1, 21, 471, 1361, 1159, 656, 562, 446, 657, 663, 612, 402, 502, 1088, 1328, 1052, 554, 433, 512, 399, 68, 3, 0, 0, 0, 16, 397, 1338, 1072, 647, 646, 532, 672, 584, 504, 417, 610, 1040, 1369, 1143, 631, 500, 611, 404, 75, 3, 0, 0, 0, 20, 497, 1248, 1080, 744, 570, 465, 672, 552, 527, 371, 614, 915, 1330, 1169, 631, 446, 529, 363, 84, 1, 0, 0, 0, 26, 429, 1258, 1148, 691, 522, 500, 645, 621, 632, 440, 582, 1134, 1094, 901, 751, 574, 434, 376, 85, 6, 0, 0, 0, 14, 130, 371, 469, 249, 267, 272, 352, 437, 397, 400, 474, 508, 449, 403, 317, 243, 166, 262, 70, 10, 0, 0, 0, 10, 84, 146, 225, 226, 279, 216, 172, 213, 243, 139, 255, 204, 277, 174, 116, 214, 219, 99, 45, 6, 0, 0, 0, 16, 513, 1218, 1178, 718, 579, 445, 664, 660, 528, 437, 509, 1010, 1374, 906, 581, 461, 601, 408, 68, 0, 0, 0, 0, 21, 441, 1413, 1193, 684, 571, 500, 639, 563, 547, 426, 453, 1042, 1230, 1198, 594, 487, 568, 398, 107, 0, 0, 0, 0, 27, 484, 1335, 1118, 736, 585, 519, 726, 645, 524, 501, 570, 1000, 1328, 1256, 644, 436, 635, 435, 79, 4, 0, 0, 0, 16, 472, 1412, 1071, 649, 572, 501, 615, 559, 476, 363, 561, 987, 1249, 1254, 742, 505, 514, 437, 70, 36, 0, 0, 0, 25, 450, 1274, 1189, 637, 584, 447, 654, 657, 550, 398, 557, 1061, 1262, 1067, 730, 461, 458, 416, 85, 5, 0, 0, 0, 26, 169, 482, 505, 374, 320, 307, 336, 432, 330, 465, 499, 484, 456, 406, 317, 212, 229, 277, 63, 11, 0, 0, 0, 13, 79, 177, 200, 281, 276, 237, 159, 286, 162, 189, 266, 305, 260, 260, 201, 235, 222, 114, 55, 5, 0, 0, 0, 17, 109, 211, 228, 203, 216, 185, 165, 163, 220, 213, 325, 392, 326, 329, 194, 180, 210, 171, 63, 8, 0, 0, 0, 20, 450, 1347, 1058, 729, 540, 485, 567, 602, 601, 435, 509, 1099, 1143, 1091, 691, 478, 569, 399, 63, 3, 0, 0, 0, 23, 504, 1272, 1204, 670, 593, 478, 702, 596, 523, 458, 536, 1079, 1212, 1194, 368, 251, 110, 69, 24, 1, 0, 0, 0, 24, 491, 1282, 1095, 729, 536, 552, 694, 588, 501, 394, 604, 1053, 1198, 1106, 660, 464, 528, 393, 95, 6, 0, 0, 0, 22, 425, 1319, 1048, 702, 475, 392, 577, 615, 562, 502, 594, 1084, 1206, 973, 657, 440, 481, 375, 71, 7, 0, 0, 0, 29, 170, 464, 498, 393, 366, 254, 366, 502, 479, 481, 493, 585, 408, 394, 288, 109, 7, 0, 0, 0, 0, 0, 0, 4, 77, 167, 200, 209, 229, 266, 167, 161, 118, 195, 210, 315, 252, 104, 16, 48, 40, 1, 0, 0, 0, 0, 0, 30, 388, 1200, 1178, 616, 503, 444, 640, 682, 572, 519, 714, 997, 1337, 1103, 631, 471, 489, 335, 54, 1, 0, 0, 0, 13, 449, 1303, 1272, 679, 500, 546, 633, 630, 652, 560, 626, 990, 1247, 1139, 631, 499, 488, 288, 45, 0, 0, 0, 0, 23, 441, 1306, 1131, 655, 584, 499, 623, 678, 529, 508, 601, 1032, 1286, 1128, 640, 483, 538, 375, 77, 2, 0, 0, 0, 22, 318, 917, 750, 422, 277, 276, 298, 350, 377, 469, 596, 645, 818, 672, 399, 244, 259, 238, 72, 1, 0, 0, 0, 13, 69, 176, 176, 192, 143, 148, 113, 143, 109, 194, 187, 241, 175, 176, 156, 70, 121, 112, 26, 4, 0, 0, 0, 10, 102, 286, 314, 240, 154, 160, 157, 187, 171, 229, 309, 367, 307, 273, 253, 155, 192, 225, 81, 2, 0, 0, 0, 16, 66, 203, 181, 185, 152, 203, 150, 305, 185, 211, 200, 243, 412, 298, 230, 213, 232, 115, 62, 4, 0, 0, 0, 13, 446, 1284, 1149, 623, 569, 568, 670, 687, 543, 536, 621, 1011, 1328, 1117, 592, 432, 535, 363, 41, 2, 0, 0, 0, 23, 477, 1367, 1173, 713, 589, 554, 604, 748, 583, 448, 586, 1056, 1325, 1286, 646, 499, 470, 368, 57, 0, 0, 0, 0, 19, 429, 1428, 1234, 668, 546, 501, 742, 671, 460, 534, 629, 1029, 1403, 1152, 586, 379, 483, 337, 74, 1, 0, 0, 0, 22, 491, 1365, 1126, 705, 544, 513, 656, 693, 587, 480, 601, 1000, 1369, 1128, 698, 463, 540, 358, 68, 2, 0, 0, 0, 21, 412, 1216, 1168, 667, 458, 475, 591, 687, 615, 464, 670, 1212, 1338, 1129, 586, 448, 485, 337, 79, 4, 0, 0, 0, 24, 137, 453, 630, 460, 335, 395, 467, 548, 466, 550, 646, 574, 566, 498, 363, 204, 209, 241, 71, 9, 0, 0, 0, 13, 92, 171, 204, 208, 232, 195, 221, 384, 274, 174, 180, 287, 257, 164, 141, 160, 144, 64, 41, 0, 0, 0, 0, 17, 401, 1317, 1238, 671, 492, 533, 690, 687, 576, 467, 584, 1006, 1444, 1315, 607, 409, 562, 389, 58, 1, 0, 0, 0, 22, 414, 1309, 1284, 616, 559, 591, 669, 729, 575, 463, 693, 1011, 1355, 1144, 688, 463, 570, 378, 57, 1, 0, 0, 0, 19, 398, 1357, 1205, 630, 578, 557, 632, 597, 598, 454, 636, 1017, 1154, 1158, 659, 434, 595, 399, 51, 1, 0, 0, 0, 23, 466, 1277, 1181, 626, 455, 567, 618, 768, 528, 465, 656, 978, 1488, 1245, 625, 469, 517, 349, 71, 4, 0, 0, 0, 21, 398, 1147, 1089, 675, 523, 381, 485, 626, 581, 514, 690, 1017, 1384, 1112, 615, 458, 462, 359, 70, 3, 0, 0, 0, 22, 144, 454, 588, 449, 343, 262, 381, 440, 358, 489, 566, 557, 593, 360, 391, 272, 201, 203, 79, 5, 0, 0, 0, 15, 73, 199, 230, 238, 242, 193, 161, 259, 198, 181, 236, 291, 282, 248, 211, 236, 219, 110, 41, 4, 0, 0, 0, 14, 367, 1078, 984, 689, 451, 459, 635, 632, 509, 549, 541, 1031, 1361, 1046, 583, 459, 501, 358, 46, 1, 0, 0, 0, 19, 344, 1011, 1005, 691, 495, 397, 540, 674, 521, 528, 717, 980, 1445, 1266, 609, 402, 483, 351, 62, 4, 0, 0, 0, 20, 405, 1378, 1186, 629, 490, 496, 717, 675, 578, 561, 648, 1062, 1307, 1183, 643, 474, 563, 395, 61, 2, 0, 0, 0, 18, 465, 1323, 1271, 608, 476, 457, 592, 616, 463, 469, 676, 1055, 1367, 1238, 541, 468, 462, 350, 59, 3, 0, 0, 0, 15, 421, 1237, 1198, 648, 560, 538, 633, 636, 555, 474, 599, 919, 1264, 1075, 691, 473, 401, 352, 63, 5, 0, 0, 0, 22, 140, 274, 362, 239, 227, 230, 232, 251, 263, 303, 431, 408, 347, 423, 341, 183, 191, 225, 64, 17, 0, 0, 0, 10, 106, 241, 241, 290, 244, 156, 180, 202, 168, 263, 239, 319, 301, 336, 245, 220, 212, 102, 51, 8, 0, 0, 0, 19, 428, 1328, 1292, 626, 542, 475, 688, 696, 550, 482, 586, 908, 1375, 1298, 642, 458, 416, 329, 51, 1, 0, 0, 0, 22, 455, 1258, 1199, 622, 472, 518, 649, 690, 594, 516, 652, 944, 1387, 1172, 644, 491, 491, 414, 45, 1, 0, 0, 0, 22, 497, 1359, 1169, 678, 595, 533, 727, 704, 553, 528, 597, 1026, 1354, 1173, 614, 471, 540, 400, 56, 2, 0, 0, 0, 17, 417, 1280, 1304, 649, 636, 437, 620, 716, 538, 491, 638, 917, 1525, 1366, 674, 498, 455, 397, 61, 1, 0, 0, 0, 22, 425, 1210, 1174, 629, 505, 424, 608, 638, 588, 476, 609, 972, 1324, 1090, 799, 445, 518, 333, 73, 3, 0, 0, 0, 15, 151, 454, 550, 502, 329, 238, 337, 514, 379, 454, 613, 621, 632, 431, 318, 195, 209, 260, 54, 3, 0, 0, 0, 14, 75, 211, 229, 213, 221, 223, 255, 278, 200, 255, 267, 243, 399, 253, 286, 235, 209, 87, 21, 0, 0, 0, 0, 13, 307, 944, 802, 455, 397, 304, 396, 429, 468, 498, 634, 736, 1064, 980, 545, 319, 292, 341, 73, 3, 0, 0, 0, 9, 88, 245, 202, 160, 186, 192, 133, 144, 192, 244, 282, 294, 253, 278, 199, 107, 119, 96, 47, 0, 0, 0, 0, 17, 376, 1351, 1323, 713, 546, 627, 659, 629, 638, 629, 638, 994, 1293, 1170, 829, 541, 525, 330, 77, 3, 0, 0, 0, 17, 445, 1230, 1282, 737, 577, 466, 644, 702, 524, 522, 692, 1002, 1536, 1072, 847, 555, 423, 347, 55, 5, 0, 0, 0, 21, 418, 1354, 1170, 746, 559, 518, 566, 626, 634, 555, 763, 1027, 1273, 1169, 834, 445, 474, 386, 82, 3, 0, 0, 0, 22, 157, 478, 531, 448, 350, 285, 446, 421, 457, 468, 537, 555, 613, 431, 303, 244, 193, 239, 66, 6, 0, 0, 0, 13, 82, 186, 215, 240, 241, 174, 241, 225, 232, 171, 307, 386, 249, 225, 162, 203, 133, 85, 50, 3, 0, 0, 0, 20, 393, 1166, 1214, 828, 565, 542, 580, 685, 619, 465, 670, 962, 1716, 1253, 761, 503, 500, 364, 57, 3, 0, 0, 0, 23, 436, 1318, 1078, 698, 543, 596, 701, 646, 598, 532, 574, 1008, 1360, 1062, 861, 523, 490, 344, 47, 5, 0, 0, 0, 14, 430, 1238, 1067, 702, 540, 451, 603, 600, 539, 568, 649, 1065, 1395, 1100, 647, 395, 518, 280, 51, 3, 0, 0, 0, 15, 342, 1222, 1041, 609, 402, 452, 572, 630, 586, 513, 634, 951, 1445, 1158, 756, 439, 441, 391, 62, 1, 0, 0, 0, 11, 402, 1324, 1066, 623, 534, 432, 549, 615, 513, 446, 605, 1076, 1167, 922, 637, 511, 486, 312, 88, 9, 0, 0, 0, 23, 141, 446, 521, 459, 309, 309, 467, 517, 449, 475, 534, 544, 514, 293, 344, 252, 207, 334, 118, 10, 0, 0, 0, 16, 100, 193, 200, 246, 246, 288, 258, 256, 180, 216, 256, 292, 345, 287, 208, 240, 213, 102, 65, 6, 0, 0, 0, 16, 416, 1329, 1193, 665, 470, 398, 657, 678, 529, 425, 595, 937, 1422, 1165, 734, 493, 491, 380, 82, 1, 0, 0, 0, 24, 436, 1323, 1139, 643, 494, 456, 660, 658, 568, 486, 584, 1019, 1384, 1259, 726, 470, 527, 402, 55, 0, 0, 0, 0, 23, 428, 1406, 1242, 672, 452, 472, 628, 600, 616, 496, 593, 956, 1242, 1239, 743, 447, 626, 358, 64, 2, 0, 0, 0, 23, 461, 1347, 1113, 602, 588, 488, 582, 684, 587, 459, 604, 982, 1353, 1008, 639, 473, 333, 320, 74, 1, 0, 0, 0, 16, 466, 1265, 1128, 618, 487, 410, 560, 633, 534, 504, 695, 953, 1340, 1115, 640, 416, 481, 347, 81, 2, 0, 0, 0, 27, 164, 529, 513, 481, 371, 255, 424, 403, 308, 392, 586, 642, 464, 311, 247, 169, 200, 245, 57, 4, 0, 0, 0, 16, 92, 191, 217, 231, 265, 193, 234, 295, 200, 266, 269, 265, 294, 232, 200, 214, 219, 95, 49, 2, 0, 0, 0, 17, 398, 1270, 1204, 600, 485, 447, 606, 617, 505, 475, 542, 1012, 1440, 1189, 634, 429, 557, 414, 41, 2, 0, 0, 0, 13, 308, 1306, 1053, 520, 548, 378, 588, 574, 461, 412, 497, 878, 1433, 1197, 632, 492, 554, 355, 86, 12, 0, 0, 0, 17, 451, 1308, 1247, 615, 460, 437, 641, 639, 551, 552, 657, 991, 1427, 1110, 714, 550, 615, 402, 63, 4, 0, 0, 0, 19, 431, 1324, 1191, 626, 524, 405, 620, 649, 551, 573, 592, 847, 1402, 930, 501, 507, 387, 331, 61, 0, 0, 0, 0, 19, 419, 1161, 1137, 726, 459, 368, 528, 572, 489, 451, 710, 945, 1282, 1046, 624, 397, 358, 306, 73, 4, 0, 0, 0, 20, 128, 469, 515, 406, 275, 280, 379, 467, 333, 303, 508, 455, 401, 386, 252, 190, 195, 268, 57, 3, 0, 0, 0, 14, 66, 175, 238, 227, 198, 171, 158, 262, 184, 207, 245, 260, 263, 214, 175, 191, 239, 133, 48, 2, 0, 0, 0, 19, 483, 1218, 1165, 514, 432, 353, 431, 475, 431, 490, 556, 905, 1212, 993, 572, 294, 325, 341, 42, 2, 0, 0, 0, 20, 443, 1365, 1295, 641, 526, 458, 639, 625, 434, 542, 688, 965, 1341, 1159, 674, 450, 450, 295, 52, 7, 0, 0, 0, 11, 441, 1317, 1243, 705, 578, 505, 604, 604, 563, 533, 658, 934, 1268, 1181, 765, 483, 478, 375, 68, 3, 0, 0, 0, 12, 127, 250, 280, 179, 227, 150, 175, 185, 214, 300, 335, 307, 271, 256, 207, 102, 126, 173, 52, 5, 0, 0, 0, 20, 394, 1089, 986, 591, 565, 435, 478, 539, 506, 506, 579, 987, 1148, 897, 578, 359, 383, 358, 73, 3, 0, 0, 0, 24, 132, 472, 491, 396, 335, 276, 340, 404, 412, 410, 470, 429, 594, 240, 375, 236, 204, 254, 69, 4, 0, 0, 0, 9, 71, 157, 224, 244, 240, 190, 166, 231, 187, 240, 358, 278, 295, 218, 199, 246, 201, 158, 48]

Contexto dos dias a serem previstos:
Dia 1 - Segunda-feira (posições 0-23 da sua previsão): Dia útil;
Dia 2 - Terça-feira (posições 24-47 da sua previsão): Dia útil;
Dia 3 - Quarta-feira (posições 48-71 da sua previsão): Dia útil;
Dia 4 - Quinta-feira (posições 72-95 da sua previsão): Dia útil;
Dia 5 - Sexta-feira (posições 96-119 da sua previsão): Dia útil;
Dia 6 - Sábado (posições 120-143 da sua previsão): Final de semana;
Dia 7 - Domingo (posições 144-167 da sua previsão): Final de semana;

Gere um array contendo os próximos 168 (N=168) números da sequência:" > {temp_file}""")

# Lê a saída do arquivo temporário
with open(temp_file, 'r') as file:
    resposta = file.read().strip()

# Imprime a resposta
print(resposta)