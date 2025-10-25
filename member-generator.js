// Générateur de pages de membres
function generateMemberPage(member) {
    const memberHtml = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${member.name} - JeunAct</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #8B1538 0%, #E91E63 100%);
            min-height: 100vh;
            margin: 0;
        }
        .member-card {
            background: white;
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            margin: 20px;
            max-width: 500px;
            margin: 20px auto;
        }
        .member-header {
            background: linear-gradient(135deg, #8B1538 0%, #E91E63 100%);
            padding: 40px 30px;
            text-align: center;
            color: white;
            position: relative;
        }
        .member-photo {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 5px solid rgba(255,255,255,0.3);
            object-fit: cover;
            margin-bottom: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .member-name {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .member-role {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid rgba(255,255,255,0.5);
            border-radius: 25px;
            padding: 8px 20px;
            font-size: 1rem;
            font-weight: 600;
            display: inline-block;
        }
        .member-body {
            padding: 40px 30px;
        }
        .social-btn {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin: 10px;
            text-decoration: none;
            color: white;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .social-btn:hover {
            transform: translateY(-5px) scale(1.05);
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .whatsapp { background: #25D366; }
        .instagram { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .linkedin { background: #0077b5; }
        .email { background: #EA4335; }
        .portfolio { background: linear-gradient(45deg, #667eea, #764ba2); }
        .facebook { background: #1877f2; }
        .tiktok { background: #000000; }
        .qr-section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            text-align: center;
        }
        .qr-code {
            background: white;
            border-radius: 10px;
            padding: 20px;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .back-btn {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.3s;
        }
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
            color: white;
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <div class="member-card">
        <div class="member-header">
            <a href="../index.html" class="back-btn">
                <i class="fas fa-arrow-left"></i>
            </a>
            ${member.photo ? `<img src="../static/photos/${member.photo}" alt="${member.name}" class="member-photo" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <div style="width: 120px; height: 120px; border-radius: 50%; border: 5px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.2); display: none; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(0,0,0,0.3); margin: 0 auto 20px;">
                <i class="fas fa-user" style="font-size: 50px; color: white;"></i>
            </div>` : `<div style="width: 120px; height: 120px; border-radius: 50%; border: 5px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(0,0,0,0.3); margin: 0 auto 20px;">
                <i class="fas fa-user" style="font-size: 50px; color: white;"></i>
            </div>`}
            <h1 class="member-name">${member.name}</h1>
            <div class="member-role">${member.role}</div>
        </div>
        
        <div class="member-body">
            <h5 class="mb-4">
                <i class="fas fa-link me-2" style="color: #8B1538;"></i>
                Contact & Réseaux
            </h5>
            
            <div class="d-flex justify-content-center flex-wrap">
                ${member.whatsapp ? `<a href="https://wa.me/${member.whatsapp}" target="_blank" class="social-btn whatsapp" title="WhatsApp">
                    <i class="fab fa-whatsapp" style="font-size: 32px;"></i>
                </a>` : ''}
                ${member.instagram ? `<a href="https://instagram.com/${member.instagram}" target="_blank" class="social-btn instagram" title="Instagram">
                    <i class="fab fa-instagram" style="font-size: 32px;"></i>
                </a>` : ''}
                ${member.linkedin ? `<a href="${member.linkedin}" target="_blank" class="social-btn linkedin" title="LinkedIn">
                    <i class="fab fa-linkedin" style="font-size: 32px;"></i>
                </a>` : ''}
                ${member.email ? `<a href="mailto:${member.email}" class="social-btn email" title="Email">
                    <i class="fas fa-envelope" style="font-size: 28px;"></i>
                </a>` : ''}
                ${member.facebook ? `<a href="https://facebook.com/${member.facebook}" target="_blank" class="social-btn facebook" title="Facebook">
                    <i class="fab fa-facebook" style="font-size: 32px;"></i>
                </a>` : ''}
                ${member.tiktok ? `<a href="https://tiktok.com/@${member.tiktok}" target="_blank" class="social-btn tiktok" title="TikTok">
                    <i class="fab fa-tiktok" style="font-size: 32px;"></i>
                </a>` : ''}
                ${member.portfolio ? `<a href="${member.portfolio}" target="_blank" class="social-btn portfolio" title="Portfolio">
                    <i class="fas fa-briefcase" style="font-size: 28px;"></i>
                </a>` : ''}
            </div>
            
            <div class="qr-section">
                <h6 class="mb-3">
                    <i class="fas fa-qrcode me-2" style="color: #8B1538;"></i>
                    Badge QR Code
                </h6>
                <div class="qr-code">
                    <div id="qrcode"></div>
                    <p class="mt-3 mb-0" style="color: #666; font-size: 0.9rem;">
                        Scannez ce QR code pour partager ce profil
                    </p>
                </div>
            </div>
            
            <div class="text-center mt-4">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">
                    <i class="fas fa-qrcode me-1" style="color: #8B1538;"></i>
                    Scanné depuis un badge JeunAct
                </p>
                <p style="color: #666; font-size: 0.85rem; margin: 0;">
                    Membre depuis - ${new Date().toLocaleDateString('fr-FR')}
                </p>
            </div>
        </div>
    </div>

    <!-- QR Code Generator -->
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>
    <script>
        // Générer le QR Code
        const qrUrl = window.location.href;
        QRCode.toCanvas(document.getElementById('qrcode'), qrUrl, {
            width: 150,
            height: 150,
            color: {
                dark: '#8B1538',
                light: '#FFFFFF'
            }
        }, function (error) {
            if (error) console.error(error);
        });
    </script>
</body>
</html>`;
    
    return memberHtml;
}

// Fonction pour créer une page de membre
function createMemberPage(memberId) {
    const member = members.find(m => m.id === memberId);
    if (member) {
        const html = generateMemberPage(member);
        
        // Créer un blob avec le HTML
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        
        // Ouvrir dans un nouvel onglet
        window.open(url, '_blank');
        
        // Nettoyer l'URL après un délai
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
}
