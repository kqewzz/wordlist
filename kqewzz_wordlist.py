#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════╗
║     WORDLIST GENERATOR PRO v2.5 - Termux Edition         ║
║     Profesyonel Şifre Kırma Wordlist Oluşturucu          ║
║     "Sosyal Mühendislik Tabanlı Wordlist Üretici"        ║
╚════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
from datetime import datetime
from itertools import combinations, permutations, product
import re

class WordlistGeneratorPro:
    def __init__(self):
        self.wordlist = set()
        self.person_data = {}
        self.output_file = None
        self.language = "tr"
        
    def banner(self):
        """Başlık göster"""
        print("\033[96m" + """
╔════════════════════════════════════════════════════════════╗
║  🎯 WORDLIST GENERATOR PRO v2.5 - Termux Edition        ║
║  📱 Şifre Kırma Wordlist Oluşturucu                      ║
║  👤 Sosyal Mühendislik Tabanlı Üretici                   ║
║  💪 Multi-Kombinasyon Sistemi                            ║
║  🌍 Küresel Dilçer Desteği                               ║
╚════════════════════════════════════════════════════════════╝
        """ + "\033[0m")
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def colored_print(self, text, color="default"):
        """Renkli yazı"""
        colors = {
            "green": "\033[92m",
            "red": "\033[91m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "cyan": "\033[96m",
            "purple": "\033[95m",
            "default": "\033[0m"
        }
        print(f"{colors.get(color, '')}{text}\033[0m")
        
    def collect_person_data(self):
        """Kişi hakkında bilgi topla"""
        self.colored_print("\n📋 KİŞİ BİLGİLERİ TOPLAMA FORMU", "cyan")
        print("-" * 60)
        
        # Ad
        self.person_data['ad'] = input("👤 Adı (örn: Ahmet): ").strip().lower()
        
        # Soyad
        self.person_data['soyad'] = input("👤 Soyadı (örn: Yılmaz): ").strip().lower()
        
        # Memleketler
        self.colored_print("\n🌍 Memleket (virgülle ayırarak yazın, örn: istanbul,ankara,izmir):", "yellow")
        memleket_input = input().strip().lower()
        self.person_data['memleket'] = [m.strip() for m in memleket_input.split(',')]
        
        # TC Kimlik Numarası (son 4 hanesi)
        tc_input = input("🆔 TC Kimlik Numarası (son 4 hanesi, örn: 1234): ").strip()
        self.person_data['tc_last4'] = tc_input if tc_input.isdigit() else "0000"
        
        # Doğum Tarihi
        birth_input = input("📅 Doğum Tarihi (GG/AA/YYYY, örn: 15/03/1990): ").strip()
        self.person_data['birth'] = birth_input
        
        # Telefon Numarası (son 4 hanesi)
        phone_input = input("📱 Telefon Numarası (son 4 hanesi, örn: 5678): ").strip()
        self.person_data['phone_last4'] = phone_input if phone_input.isdigit() else "0000"
        
        # Email
        self.person_data['email'] = input("📧 Email Adresi (örn: ahmet@example.com): ").strip().lower()
        
        # Evcil Hayvan Adı
        self.person_data['pet'] = input("🐕 Evcil Hayvan Adı (örn: Boncuk): ").strip().lower()
        
        # Hobi/İlgi Alanları
        self.colored_print("🎮 Hobi/İlgi Alanları (virgülle ayırarak, örn: futbol,müzik,oyun):", "yellow")
        hobi_input = input().strip().lower()
        self.person_data['hobi'] = [h.strip() for h in hobi_input.split(',')]
        
        # Sevdiği Ünlüler
        self.colored_print("⭐ Sevdiği Ünlüler (virgülle ayırarak):", "yellow")
        celebs_input = input().strip().lower()
        self.person_data['celebrities'] = [c.strip() for c in celebs_input.split(',')]
        
        # Sevdiği Şarkılar/Filmler
        self.person_data['favorite'] = input("🎬 Sevdiği Şarkı/Film Başlıkları (virgülle ayırarak): ").strip().lower()
        
        # Şirket/Okul Adı
        self.person_data['company'] = input("🏢 Çalıştığı Şirket/Okul (örn: Microsoft): ").strip().lower()
        
        self.colored_print("\n✅ Veriler kaydedildi!", "green")
        
    def generate_wordlist(self):
        """Wordlist oluştur"""
        self.colored_print("\n🔧 WORDLIST OLUŞTURULUYOR...", "cyan")
        
        # Temel veriler
        base_words = []
        
        # Ad ve Soyad
        base_words.append(self.person_data['ad'])
        base_words.append(self.person_data['soyad'])
        base_words.append(self.person_data['ad'] + self.person_data['soyad'])
        base_words.append(self.person_data['soyad'] + self.person_data['ad'])
        
        # Memleketler
        base_words.extend(self.person_data['memleket'])
        
        # Hobi
        base_words.extend(self.person_data['hobi'])
        
        # Ünlüler
        base_words.extend(self.person_data['celebrities'])
        
        # Şirket
        base_words.append(self.person_data['company'])
        
        # Evcil hayvan
        if self.person_data['pet']:
            base_words.append(self.person_data['pet'])
        
        # Tarihi verileri
        if self.person_data['birth']:
            dates = self.person_data['birth'].split('/')
            base_words.extend(dates)
            base_words.append(self.person_data['birth'].replace('/', ''))
            base_words.append(dates[2] + dates[1] + dates[0])
        
        # Numari veriler
        base_words.append(self.person_data['tc_last4'])
        base_words.append(self.person_data['phone_last4'])
        
        # Email parçaları
        email_parts = self.person_data['email'].split('@')[0].split('.')
        base_words.extend(email_parts)
        
        # Favorileri
        favorites = self.person_data['favorite'].split(',')
        base_words.extend([f.strip().lower() for f in favorites])
        
        # Özel karakterler kaldır ve filtrele
        base_words = [w for w in base_words if w and len(w) > 0]
        self.wordlist.update(base_words)
        
        print(f"   └─ Temel kelimeler: {len(base_words)}")
        
        # Kombinasyonlar
        self._generate_combinations(base_words)
        
        # Mutasyonlar
        self._generate_mutations(base_words)
        
        # Sayı suffixleri
        self._generate_with_numbers(base_words)
        
        # Özel karakterler
        self._generate_special_chars(base_words)
        
        # Leet speak
        self._generate_leet_speak(base_words)
        
        self.colored_print(f"\n✅ Toplam Wordlist: {len(self.wordlist)} kelime", "green")
        
    def _generate_combinations(self, words):
        """Kelime kombinasyonları"""
        print("   └─ Kombinasyonlar üretiliyor...")
        count = 0
        
        for word1, word2 in combinations(words, 2):
            if len(word1) > 0 and len(word2) > 0:
                self.wordlist.add(word1 + word2)
                self.wordlist.add(word2 + word1)
                self.wordlist.add(word1 + "-" + word2)
                self.wordlist.add(word2 + "-" + word1)
                count += 4
                
                if count > 10000:
                    break
        
        print(f"      └─ {count} kombinasyon eklendi")
        
    def _generate_mutations(self, words):
        """Kelime mutasyonları"""
        print("   └─ Mutasyonlar üretiliyor...")
        count = 0
        
        mutations = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            'l': ['1'],
            't': ['7'],
            'z': ['2']
        }
        
        for word in words[:50]:
            mutated = word
            for original, replacements in mutations.items():
                for replacement in replacements:
                    mutated = word.replace(original, replacement)
                    if mutated != word:
                        self.wordlist.add(mutated)
                        count += 1
        
        print(f"      └─ {count} mutasyon eklendi")
        
    def _generate_with_numbers(self, words):
        """Sayı suffixleri ekle"""
        print("   └─ Sayı suffixleri ekleniyor...")
        count = 0
        
        for word in words:
            for num in range(100):
                self.wordlist.add(word + str(num))
                self.wordlist.add(str(num) + word)
                count += 2
        
        print(f"      └─ {count} sayı kombinasyonu eklendi")
        
    def _generate_special_chars(self, words):
        """Özel karakterler ekle"""
        print("   └─ Özel karakterler ekleniyor...")
        count = 0
        
        special_chars = ['!', '@', '#', '$', '%', '&', '*', '.', '-', '_']
        
        for word in words[:30]:
            for char in special_chars:
                self.wordlist.add(word + char)
                self.wordlist.add(char + word)
                count += 2
        
        print(f"      └─ {count} özel karakter kombinasyonu eklendi")
        
    def _generate_leet_speak(self, words):
        """Leet speak dönüşümü"""
        print("   └─ Leet speak çeşitleri üretiliyor...")
        count = 0
        
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5',
            'l': '1', 't': '7', 'z': '2', 'g': '9', 'b': '8'
        }
        
        for word in words[:30]:
            for old, new in leet_map.items():
                if old in word:
                    leet_word = word.replace(old, new)
                    self.wordlist.add(leet_word)
                    self.wordlist.add(leet_word.upper())
                    count += 2
        
        print(f"      └─ {count} leet speak çeşidi eklendi")
        
    def save_wordlist(self):
        """Wordlist'i dosyaya kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wordlist_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in sorted(self.wordlist):
                    f.write(word + '\n')
            
            self.colored_print(f"\n✅ Wordlist kaydedildi: {filename}", "green")
            self.colored_print(f"   └─ Toplam kelime: {len(self.wordlist)}", "green")
            
            # Dosya bilgileri
            file_size = os.path.getsize(filename) / 1024
            self.colored_print(f"   └─ Dosya boyutu: {file_size:.2f} KB", "green")
            
            self.output_file = filename
            
        except Exception as e:
            self.colored_print(f"❌ Hata: {str(e)}", "red")
            
    def show_statistics(self):
        """İstatistikler göster"""
        self.colored_print("\n📊 WORDLIST İSTATİSTİKLERİ", "cyan")
        print("-" * 60)
        
        lengths = {}
        for word in self.wordlist:
            length = len(word)
            lengths[length] = lengths.get(length, 0) + 1
        
        print(f"📈 Toplam Kelime: {len(self.wordlist)}")
        print(f"📏 En Kısa: {min(len(w) for w in self.wordlist)} karakter")
        print(f"📏 En Uzun: {max(len(w) for w in self.wordlist)} karakter")
        print(f"📊 Ortalama: {sum(len(w) for w in self.wordlist) / len(self.wordlist):.1f} karakter")
        
        print(f"\n📊 Uzunluk Dağılımı:")
        for length in sorted(lengths.keys())[:10]:
            print(f"   {length} karakter: {lengths[length]} kelime")
            
    def run(self):
        """Ana program"""
        self.clear_screen()
        self.banner()
        
        try:
            self.collect_person_data()
            self.generate_wordlist()
            self.show_statistics()
            self.save_wordlist()
            
            self.colored_print("\n🎉 İşlem Tamamlandı!", "green")
            
        except KeyboardInterrupt:
            self.colored_print("\n⚠️  Program kapatıldı.", "yellow")
        except Exception as e:
            self.colored_print(f"\n❌ Hata oluştu: {str(e)}", "red")

if __name__ == "__main__":
    generator = WordlistGeneratorPro()
    generator.run()

