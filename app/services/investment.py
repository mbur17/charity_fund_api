from datetime import datetime

from app.models import CharityProject, Donation


def invest(
    projects: list[CharityProject],
    donations: list[Donation]
) -> None:
    """Универсальная функция инвестирования."""
    for project in projects:
        if project.fully_invested:
            continue
        for donation in donations:
            if donation.fully_invested:
                continue

            available_donation = (
                donation.full_amount - donation.invested_amount
            )
            required_amount = project.full_amount - project.invested_amount
            amount = min(available_donation, required_amount)

            donation.invested_amount += amount
            project.invested_amount += amount

            if donation.invested_amount >= donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()

            if project.invested_amount >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()

            if project.fully_invested:
                break
