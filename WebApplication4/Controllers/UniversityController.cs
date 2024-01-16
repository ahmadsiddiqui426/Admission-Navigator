// Controllers/UniversityController.cs
using ConsoleApp1.Data;
using Microsoft.AspNetCore.Mvc;
using System.Linq;

public class UniversityController : Controller
{
    private readonly UniContext _context;

    public UniversityController(UniContext context)
    {
        _context = context;
    }

    public IActionResult Details(int fieldId)
    {
        var universities = _context.FieldUniversities
            .Where(fu => fu.FID == fieldId)
            .Select(fu => fu.University)
            .ToList();

        return View(universities);
    }
}
