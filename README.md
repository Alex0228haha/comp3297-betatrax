# BetaTrax

Defect tracking system for beta testing.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install django djangorestframework
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

### Tester
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/defects/` | Submit defect report |

### Product Owner
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/po/defects/new/` | List New defects |
| GET | `/api/po/defects/<id>/` | View defect details |
| POST | `/api/po/defects/<id>/approve/` | Approve defect (New → Open) |
| PATCH | `/api/defects/<id>/resolve/` | Close defect (Fixed → Resolved) |

### Developer
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/developer/defects/open/` | List Open defects |
| GET | `/api/developer/defects/<id>/` | View defect details |
| POST | `/api/developer/defects/<id>/take-responsibility/` | Take responsibility (Open → Assigned) |
| POST | `/api/developer/defects/<id>/mark-as-fixed/` | Mark as fixed (Assigned → Fixed) |
| POST | `/api/developer/defects/<id>/mark-as-cannot-reproduce/` | Mark as cannot reproduce |

## Working Features

- [x] Submit defect report with optional email
- [x] PO view and list New defects
- [x] PO accept defect with Severity/Priority
- [x] Developer view and list Open defects
- [x] Developer take responsibility for defect
- [x] Developer mark defect as Fixed
- [x] Developer mark defect as Cannot Reproduce
- [x] PO close defect as Resolved
- [x] Email notifications (console backend)

## Not Implemented

- [ ] PO reject defect
- [ ] PO mark defect as Duplicate
- [ ] Reopen defect flow
- [ ] Comments on defects
